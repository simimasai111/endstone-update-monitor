# Endstone / LeviLamina 更新日志



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

