# -*- coding: utf-8 -*-
"""明日方舟语音 .ab 解包脚本（含 LZ4AK 修正）

从《明日方舟》Unity AssetBundle 语音文件（含 2025 年后 v2.5.04+ 新版
自定义压缩）中提取 AudioClip 为 .wav。LZ4AK 算法取自
isHarryh/Ark-Unpacker（BSD-3-Clause），致谢 Harry Huang / Kengxxiao /
MooncellWiki: UnityPy。
"""
import os
import sys

import lz4.block
import UnityPy
from UnityPy.enums.BundleFile import CompressionFlags
from UnityPy.helpers import CompressionHelper


def _read_extra_length(data, pos, max_pos):
    """连续读取 0xFF 雪球长度字段。"""
    extra = 0
    while pos < max_pos:
        b = data[pos]
        extra += b
        pos += 1
        if b != 0xFF:
            break
    return extra, pos


def decompress_lz4ak(compressed, uncompressed_size):
    """LZ4AK：高低半字节换位后的 LZ4 块解压。"""
    data = bytearray(compressed)
    size = len(data)
    ip = op = 0
    while ip < size:
        ll = data[ip] & 0xF        # literal length（低半字节）
        ml = (data[ip] >> 4) & 0xF  # match length（高半字节）
        data[ip] = (ll << 4) | ml   # 换位还原为 LZ4 标准布局
        ip += 1
        if ll == 0xF:
            extra, ip = _read_extra_length(data, ip, size)
            ll += extra
        ip += ll
        op += ll
        if op >= uncompressed_size:
            break
        offset = (data[ip] << 8) | data[ip + 1]
        data[ip] = offset & 0xFF
        data[ip + 1] = (offset >> 8) & 0xFF
        ip += 2
        if ml == 0xF:
            extra, ip = _read_extra_length(data, ip, size)
            ml += extra
        ml += 4
        op += ml
    return lz4.block.decompress(bytes(data), uncompressed_size)


# 用 LZ4AK 覆盖 UnityPy 对 LZHAM 压缩的默认解压（原版处理不了）
CompressionHelper.DECOMPRESSION_MAP[CompressionFlags.LZHAM] = decompress_lz4ak


def unpack(ab_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    count = 0
    for obj in UnityPy.load(ab_path).objects:
        if obj.type.name != "AudioClip":
            continue
        samples = obj.read().samples or {}
        for name, raw in samples.items():
            with open(os.path.join(out_dir, name), "wb") as f:
                f.write(raw)
            count += 1
    print(f"[OK] {os.path.basename(ab_path)} -> {out_dir}  ({count} audio(s))")
    return count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <input.ab> [...] <output_dir>")
    out_dir = sys.argv[-1]
    for ab in sys.argv[1:-1]:
        try:
            unpack(ab, out_dir)
        except Exception:
            print(f"[FAIL] {ab}: {sys.exc_info()[1]}")
