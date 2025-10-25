# Some basic analysis of the "disk" image

## file
```bash
SD_Card.img:
  DOS/MBR boot sector,
  code offset 0x3c+2,
  OEM-ID "mkfs.fat",
  sectors/cluster 4,
  reserved sectors 4,
  root entries 512,
  sectors 40960 (volumes <=32 MB),
  Media descriptor 0xf8,
  sectors/FAT 40,
  sectors/track 32,
  heads 64,
  hidden sectors 2048,
  reserved 0x1,
  serial number 0xaaf966d1,
  label: "PHOTOS     ",
  FAT (16 bit)
```

## fdisk
```bash
Disk SD_Card.img: 20 MiB, 20971520 bytes, 40960 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x00000000
```

## binwalk
```bash
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
61440         0xF000          PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
61481         0xF029          Zlib compressed data, default compression
1982464       0x1E4000        PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
1982616       0x1E4098        Zlib compressed data, default compression
4315136       0x41D800        PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
4315288       0x41D898        Zlib compressed data, default compression
6201344       0x5EA000        PNG image, 819 x 1227, 8-bit/color RGBA, non-interlaced
8198144       0x7D1800        PNG image, 851 x 1275, 8-bit/color RGBA, non-interlaced
8198185       0x7D1829        Zlib compressed data, default compression
9164769       0x8BD7E1        MySQL MISAM compressed data file Version 10
```
## fls
```bash
r/r 3:	PHOTOS      (Volume Label Entry)
r/r 5:	beach.png
r/r 8:	best_friend.png
r/r 10:	biking.png
r/r 12:	ice_cream.png
r/r * 14:	mystery.jpg                <---- JUICY
r/r 16:	sherLOCH.png
v/v 654019:	$MBR
v/v 654020:	$FAT1
v/v 654021:	$FAT2
V/V 654022:	$OrphanFiles
```
