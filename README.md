# 明日方舟语音 `.ab` 解包工具

将《明日方舟》的语音资源包 `.ab` 提取为 `.wav` 文件，支持中文和日文语音。

适用资源路径：

```text
Arknights_Data\PersistentData\Bundles\audio\sound_beta_2\voice\*.ab
```

支持 2025 年后（v2.5.04 及以上版本）的新版自定义压缩资源。

## 依赖

- Python 3.8+
- [UnityPy](https://github.com/K0lb3/UnityPy)
- [lz4](https://github.com/python-lz4/python-lz4)

```powershell
python -m pip install UnityPy lz4
```

## 使用

```powershell
python unpack_ab_audio.py <输入.ab> <输出目录>
```

例如：

```powershell
python unpack_ab_audio.py "D:\游戏资源\char_4182_oblvns.ab" .\out_4182
```

支持一次处理多个资源包，最后一个参数作为输出目录：

```powershell
python unpack_ab_audio.py "D:\语音\a.ab" "D:\语音\b.ab" .\out
```

输出目录中会生成 `CN_001.wav`、`JP_001.wav` 等语音文件。多个资源包包含同名文件时，后处理的文件会覆盖先处理的文件。

## 常见问题

如果出现 `Custom compression` 或 `LZHAM` 错误，请确认输入文件完整，且资源包未在复制或下载过程中损坏。脚本已内置新版资源使用的 LZ4AK 解压修正。

## 致谢

LZ4AK 解压算法参考自 [Ark-Unpacker](https://github.com/isHarryh/Ark-Unpacker)，遵循 BSD-3-Clause 许可证。
