
import datetime
from contextlib import suppress
from Bot.DatacoreBot import DatacoreBot
import pomice
import discord
from discord.ext import commands
import logging
log = logging.getLogger("Datacore")

def sec_to_min(time: float):
    time = round(time)
    hours, seconds = divmod(time, 60 * 60)
    minutes, seconds = divmod(seconds, 60)
    if not hours:
        return f"{minutes}m {str(seconds).zfill(2)}s"
    return f"{hours}h {minutes}m {str(seconds).zfill(2)}s"


async def fetch_or_get_message(client: discord.Bot, message_id: int, channel_id: int) -> discord.Message:
    message = client.get_message(message_id)
    if message is not None:
        return message
    else:
        partial_msg = client.get_partial_messageable(channel_id)
        return await partial_msg.fetch_message(message_id)


class DragonQueue(pomice.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.history: list[pomice.Track] = []
        self.last_track: pomice.Track = None




loop_emoji = {"Off": ":arrow_right:", "Track": ":repeat_one:", "Queue": ":repeat:"}


class DragonPlayer(pomice.Player):
    """Custom pomice Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = DragonQueue()
        self.controller: discord.Message = None
        # Set context here, so we can send a now playing embed
        self.context: commands.Context = None
        self.dj: discord.Member = None

    async def do_next(self) -> None:
        # Queue up the next track, else teardown the player
        try:
            track: pomice.Track = self.queue.get()
        except pomice.QueueEmpty:
            return await self.controller.edit(embed=discord.Embed(title="Queue empty", color=discord.Color.blurple()))

        await self.play(track)

    async def update_embed(self, upcoming_tracks: list[pomice.Track] = None) -> None:
        queue: list[pomice.Track] = self.queue.get_queue()
        track: pomice.Track = self.current if self.current is not None else queue[0]
        playing_until = 0
        playing_until += self.current.length if self.current is not None else 0
        for t in queue:
            playing_until += t.length
        until = datetime.datetime.now() + datetime.timedelta(milliseconds=playing_until)
        until = until.strftime("%H:%M")

        loop_mode = self.queue.loop_mode
        if loop_mode is pomice.LoopMode.TRACK:
            loop_mode = "Track"
        elif loop_mode is pomice.LoopMode.QUEUE:
            loop_mode = "Queue"
        else:
            loop_mode = "Off"

        embed = discord.Embed(title=f"Now playing", description=f"""[{track.title}]({track.uri})
                            Duration: {sec_to_min(track.length / 1000)} :hourglass_flowing_sand:
                            Author: {track.author} :notes:
                            Playing until: {until if loop_mode == "Off" else "To infinity :infinity:"} :clock3:
                            Loop: {loop_mode} {loop_emoji[loop_mode]}
                        """, color=discord.Color.blurple(), )
        embed.set_image(url=track.thumbnail)
        embed.set_footer(text=f"Requested by {track.requester.name}#{track.requester.discriminator}",
            icon_url=track.requester.display_avatar.url, )

        if upcoming_tracks is None:
            for i in range(5):
                now_fields = len(embed.fields)
                if now_fields > 4:
                    break
                try:
                    track = queue[i]
                    embed.add_field(name=f"{now_fields + 1}. in queue",
                        value=f"[{track.title}]({track.uri})\n-> {track.author} :notes:\n-> {sec_to_min(track.length / 1000)}  :hourglass_flowing_sand:",
                        inline=False, )
                except IndexError:
                    break
        else:
            for i in range(5):
                now_fields = len(embed.fields)
                if now_fields > 4:
                    break
                try:
                    track = upcoming_tracks[i]
                    embed.add_field(name=f"{now_fields + 1}. in queue",
                        value=f"[{track.title}]({track.uri})\n-> {track.author} :notes:\n-> {sec_to_min(track.length / 1000)}  :hourglass_flowing_sand:",
                        inline=False, )
                except IndexError:
                    break
        await self.controller.edit(embed=embed)

    async def set_context(self, ctx: commands.Context):
        """Set context for the player"""
        self.context = ctx
        self.dj = ctx.author

    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""
        with suppress(discord.HTTPException, KeyError):
            await self.destroy()
            if self.controller:
                await self.controller.delete()

    async def get_controller(self):
        return self.controller


class MusicPlayerCog(commands.Cog):
    def __init__(self, client):
        self.client: DatacoreBot = client

    music = discord.SlashCommandGroup(
        name="music",
        description="all commands referring to the music part",
    )

    @music.command(name="play", description="Play a song you want to play.")
    async def play(
        self,
        ctx: discord.ApplicationContext,
        search: discord.Option(
            description="Just type what song you want to play and I will search it."
        ),
    ) -> None:
        responded = False
        if not ctx.voice_client:
            channel = getattr(ctx.user.voice, "channel", None)
            if not channel:
                raise commands.CheckFailure(
                    "You must be in a voice channel to use this command"
                    "without specifying the channel argument."
                )

            vc: DragonPlayer = await ctx.author.voice.channel.connect(cls=DragonPlayer)
            await vc.set_volume(25)
            await ctx.response.send_message(
                f"Joined the voice channel `{channel}`", delete_after=10
            )
            await self.client.ws.voice_state(
                guild_id=ctx.guild_id,
                channel_id=ctx.voice_client.channel.id,
                self_deaf=True,
            )
            responded = True

        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not add a song when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )

        await player.set_context(ctx)
        search_em = discord.Embed(
            title=f"Searching for {search}...", color=discord.Color.blurple()
        )
        if responded:
            msg = await ctx.send(embed=search_em)
        else:
            msg = await ctx.response.send_message(embed=search_em)
        results = await player.get_tracks(query=f"{search}", ctx=ctx)
        if player.controller is None:
            if responded:
                player.controller = msg
            else:
                player.controller = msg.message
        else:
            if responded:
                await msg.delete(delay=5)
            else:
                await msg.delete_original_response(delay=5)

        if not results:
            raise commands.CommandError("No results were found for that search term.")

        if isinstance(results, pomice.Playlist):
            player.queue.extend(results.tracks)
            await player.update_embed()
            if not player.is_playing:
                await player.do_next()
        else:
            track = results[0]
            player.queue.put(track)
            await player.update_embed()
            if not player.is_playing:
                await player.do_next()

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState,
    ):
        if member != self.client.user:
            return
        if member == self.client.user:
            if after is None:
                vc: DragonPlayer = member.guild.voice_client
                await vc.teardown()
                print("teared_down")
            else:
                guild = member.guild
                guild.voice_client.channel = after.channel

    @commands.Cog.listener()
    async def on_pomice_track_start(self, player: DragonPlayer, track: pomice.Track):
        loop_mode = player.queue.loop_mode
        upcoming = []

        if loop_mode is pomice.LoopMode.TRACK:
            upcoming.append(track)

        elif loop_mode is pomice.LoopMode.QUEUE:
            queue = player.queue.get_queue()
            current = player.queue.find_position(track)
            for t in queue:
                walker = player.queue.find_position(t)
                if walker < current:
                    pass
                else:
                    upcoming.append(t)
            if len(upcoming) < 5:
                for missing in range(5 - len(upcoming)):
                    upcoming.append(queue[missing])

        else:
            queue = player.queue.get_queue()
            for i in range(5):
                try:
                    upcoming.append(queue[i])
                except IndexError:
                    break
        await player.update_embed(
            upcoming_tracks=(upcoming if upcoming is not False else None)
        )

    @commands.Cog.listener()
    async def on_pomice_track_end(
            self, player: DragonPlayer, track: pomice.Track, reason: str
    ):
        await player.do_next()
        player.queue.history.append(track)
        if len(player.queue.history) > 10:
            player.queue.history.pop(0)

    @commands.Cog.listener()
    async def on_pomice_track_exception(
            self, player: DragonPlayer, error_code, exception
    ):
        log.error(f"Pomice exception: {player.guild.name}: {error_code} | {exception} ")
        await player.controller.channel.send(f"Track errored skipping...")
        await player.do_next()

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: DragonPlayer, track: pomice.Track):
        await player.controller.channel.send(
            f"Track got stuck {track.title}\nto put it back in queue use /play {track.title}"
        )

    @music.command(name="join", description="Joins your voice channel")
    async def join_cmd(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            channel = getattr(ctx.user.voice, "channel", None)
            if not channel:
                raise commands.CheckFailure(
                    "You must be in a voice channel to use this command"
                    "without specifying the channel argument."
                )

            vc: DragonPlayer = await ctx.author.voice.channel.connect(cls=DragonPlayer)
            await vc.set_volume(25)
            await ctx.response.send_message(
                f"Joined the voice channel `{channel}`", delete_after=10
            )
            await self.client.ws.voice_state(
                guild_id=ctx.guild_id,
                channel_id=ctx.voice_client.channel.id,
                self_deaf=True,
            )
        else:
            await ctx.response.send_message(
                f"I can't join your voice channel I am already connected to {ctx.voice_client.channel}",
                delete_after=10,
                ephemeral=True,
            )

    @music.command(
        name="loop", description="Sets a loop for the current queue"
    )
    async def loop_cmd(
            self,
            ctx: discord.ApplicationContext,
            loop_mode: discord.Option(
                str,
                choices=[
                    discord.OptionChoice("Off"),
                    discord.OptionChoice("Track"),
                    discord.OptionChoice("Queue"),
                ],
            ),
    ):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't set a loop when I am not playing a song!",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
                ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not loop the queue when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        if loop_mode == "Off":
            player.queue.disable_loop()
            return await ctx.response.send_message(
                f"Loop mode set to off",
                ephemeral=True,
                delete_after=10,
            )
        if loop_mode == "Track":
            player.queue.set_loop_mode(pomice.LoopMode.TRACK)
            return await ctx.response.send_message(
                f"Loop mode set to Track",
                ephemeral=True,
                delete_after=10,
            )
        if loop_mode == "Queue":
            player.queue.set_loop_mode(pomice.LoopMode.QUEUE)
            return await ctx.response.send_message(
                f"Loop mode set to Queue",
                ephemeral=True,
                delete_after=10,
            )
        else:
            log.critical("Invalid loop mode set!")

    @music.command(name="skip", description="Skip the currently playing song")
    async def skip_cmd(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't skip a song I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
                ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not skip a song when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        await ctx.response.send_message(
            f"Skipped {player.current}", ephemeral=True, delete_after=10
        )
        controller: discord.Message = player.controller
        await controller.channel.send(
            embed=discord.Embed(color=discord.Color.blurple()).set_author(
                name=f"{ctx.author.display_name} skipped {player.current}",
                icon_url=ctx.author.display_avatar.url,
                url=player.current.uri,
            ),
            delete_after=10,
        )
        await player.stop()

    @music.command(name="stop", description="Stop the playback entirely")
    async def skip_cmd(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't stop a playback if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
                ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not stop the player when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        await player.teardown()
        await player.controller.channel.send(
            f"{ctx.author.display_name}#{ctx.author.discriminator} stopped the player."
        )
        await ctx.response.send_message(
            f"You stopped the player.", ephemeral=True, delete_after=10
        )

    @music.command(
        name="set_volume", description="Set's the volume to a desired number"
    )
    async def volume_cmd(
            self,
            ctx: discord.ApplicationContext,
            volume: discord.Option(int, description="Set your desired volume"),
    ):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't change the volume if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
                ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not change the volume when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        try:
            vol = int(volume)
        except ValueError:
            return await ctx.response.send_message(
                "You may not use anything else than numbers between 0 and 500",
                delete_after=10,
                ephemeral=True,
            )
        if not 0 < vol < 501:
            return await ctx.response.send_message(
                "You may not use anything else than numbers between 0 and 500",
                delete_after=10,
                ephemeral=True,
            )
        await player.set_volume(vol)
        return await ctx.response.send_message(
            f"You've set the volume to {vol}", delete_after=10, ephemeral=True
        )


def setup(client: DatacoreBot):
    client.add_cog(MusicPlayerCog(client))
