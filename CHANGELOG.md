# Endstone / LeviLamina 更新日志



## Endstone


### v0.11.8


发布时间:

2026-08-07


Release:

https://github.com/EndstoneMC/endstone/releases/tag/v0.11.8


更新内容:

### Fixed

- Fixed a crash on Windows when reading the item charged into a crossbow, for example through its item meta. The server called into an invalid address instead of the item's loader. Introduced in 0.11.7 along with BDS 1.26.40 support.

- Fixed clients timing out on the connection screen when the world's `LANBroadcast` flag is off. BDS then never publishes the server advertisement, so it answers the client's ping with an empty response, and recent clients refuse to start the connection handshake without a valid one. The advertisement is now restored on startup, using the `server-name` from `server.properties`. Note that a server in this state also starts using the LAN discovery ports (19132/19133) again, as it would have with the flag on. Servers hidden with `enable-lan-visibility=false` are advertised again as well (#423, #465).

**Full Changelog**: https://github.com/EndstoneMC/endstone/compare/v0.11.7...v0.11.8



---



## Endstone


### v0.11.7


发布时间:

2026-08-06


Release:

https://github.com/EndstoneMC/endstone/releases/tag/v0.11.7


更新内容:


### Added

- Added support for BDS version 1.26.40.
- Added equality comparison, hashing, and `std::format` support to `endstone::SocketAddress` (C++), so it can be used directly as a key in `std::unordered_map`/`std::unordered_set` and formatted as `hostname:port`.

### Changed

- `/reload` now waits up to 2.5 seconds for running async tasks to finish, then logs a warning naming the plugin ("Nag author(s) ...") and proceeds, matching CraftBukkit. Previously the reload tore plugins down immediately, so a still-running async task could crash the server.
- A shared library in `plugins/` without an entry point is now only reported as an error if its name starts with `endstone_`. `endstone_add_plugin` gives every plugin that prefix, so a prefixed file missing `ENDSTONE_PLUGIN` is still called out by name; anything else is treated as a library a plugin ships alongside itself and skipped quietly. Previously every such file produced a "Did you forget ENDSTONE_PLUGIN?" error, so plugins could not place their own libraries in the folder.
- Log files now show the thread name instead of a numeric thread id. Threads without a name still fall back to the id.
- `endstone_add_plugin` now builds plugins with hidden symbol visibility on Linux, so a plugin exports only its `ENDSTONE_PLUGIN` entry point, as it already did on Windows. This stops a plugin's own symbols, and those of the libraries it bundles, from colliding with the server's copies inside the BDS process. A plugin that deliberately exports more can set `CXX_VISIBILITY_PRESET default` on its target.

### Fixed

- Fixed a resource pack being applied twice when it is both listed in `world_resource_packs.json` and present as an archive in `resource_packs/`. Archives that are already on the world's pack stack are now left alone.

- Fixed memory corruption on Linux whenever a soft enum was updated, which happens every time a command's dynamic choices change. The update packet was written at the wrong offsets and overran the end of the packet.

- Fixed clients being disconnected by a custom map render when the map tracks no entities. The map packet carries its decorations and their tracked actor ids as parallel lists, and the rendered cursors were replacing only the decorations, leaving the two lists at different lengths (#459).

- Fixed events fired from a plugin's `on_load`, or from the `on_enable` of a plugin with `load: startup`, being rejected with "must be triggered synchronously from server thread". Both run before the server thread exists, so the main thread is now reported as the primary thread until it does, matching Spigot.

- Fixed every script log line being followed by a blank line in the console and log file. Script output arrives with a trailing line break, which is now stripped before the message is logged.
- Fixed the `endstone` launcher exiting with `Aborted!` and code 1 when the server is stopped with Ctrl+C. The launcher now lets the server handle Ctrl+C, waits for it to shut down gracefully, and reports its actual exit code.
- Fixed `Scheduler.is_running()` returning the opposite of the truth for async tasks: `True` while the task was idle and `False` while it was actually executing.
- Fixed a class of scheduler crashes and leaks around async tasks: a task submitted to the thread pool could be destroyed while still queued, a task cancelled at the wrong moment could still run, and tasks scheduled from another thread or from inside a task callback could leak or fire one tick early (#436).
- Fixed cancelled tasks holding on to their callbacks until their scheduled tick; they are now released on the next tick, and before plugin libraries are unloaded on `/reload`.
- Fixed `PluginLoader.disable_plugin` in Python enabling the plugin instead of disabling it.
- Fixed an access-violation crash when converting NBT data containing an empty byte array to a string, for example the item NBT of a firework star (#443).
- Fixed death messages for entity and projectile kills always showing the generic "Player died" instead of the detailed vanilla message, such as "Player was slain by Zombie". Death message overrides set on the damage source are now honored as well (#438).
- Fixed C++ plugins failing to compile against the public headers with libc++ 18, which rejected the `std::formatter` specializations due to their declared return type (#437).
- Fixed C++ plugin builds on Linux silently compiling against libstdc++ when Endstone is consumed via CMake FetchContent. The `endstone::endstone` target now propagates `-stdlib=libc++` to every target that links against it, so plugin projects no longer need to pass the flag themselves.
- Fixed the public C++ headers pulling in `<Windows.h>`, which leaked macros such as `min`, `max` and `ERROR` into every plugin that includes an Endstone header. The headers now declare the two Win32 functions they need themselves, and the `endstone::endstone` target defines `NOMINMAX` and `WIN32_LEAN_AND_MEAN`, so a `<Windows.h>` the plugin includes itself stays out of the way too.




---



## LeviLamina


### v26.20.7


发布时间:

2026-08-01


Release:

https://github.com/LiteLDev/LeviLamina/releases/tag/v26.20.7


更新内容:

### Added

- LeviLamina client's default language now follows the client's language
- Added CoroTask::via executor switching @OEOTYAN
- Implemented DDUI with session architecture and enhanced safety features #1824 @LordBombardir @OEOTYAN

### Changed

- Bumped bedrock-rumtime-data to v26.20.5-server.7 and v26.20.4-client.7
- Replaced ATL smart pointers in FontUtils @OEOTYAN

### Fixed

- Fixed DisableAllMods on client


---



## LeviLamina


### v26.20.6


发布时间:

2026-07-29


Release:

https://github.com/LiteLDev/LeviLamina/releases/tag/v26.20.6


更新内容:

### Added

- Added semantic version ranges and mod load planning @OEOTYAN
- Added batched writes to KeyValueDB @OEOTYAN
- Added constructor for SubChunkPacket::SubChunkPacketData
- Added constructor for MobEquipmentPacket
- Added `BinaryStream::write(char const* origin, uint64 num)`

### Changed

- Reverted modification for Player::getLocaleCode
- Supported named arguments in I18nStringError @zimuya4153

### Fixed

- Fixed KeyValueDB::empty() [#1822]
- Initialize mSerializationMode for some packets's constructor


---

