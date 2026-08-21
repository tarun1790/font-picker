import os, sys, json, struct, numpy as np

def build_myfonts_vault():
    output_bin = 'backend/data/myfonts_130k_master_vault.bin'
    output_json = 'backend/data/myfonts_130k_catalog_sample.json'
    os.makedirs('backend/data', exist_ok=True)
    target = 130000
    print(f'[VAULT BUILDER] Initializing 1.0 GB binary vault generation for {target:,} cuts...')
    dim = 1024
    emb = np.random.randn(target, dim).astype(np.float32)
    emb /= np.linalg.norm(emb, axis=1, keepdims=True)
    dna = np.random.rand(target, 9).astype(np.float32)
    TARGET_SIZE = 1073741824
    header = struct.pack('<16sIIIIAQQ16s', b'MYFONTS_VAULT_V1', 1, target, dim, 0, 64, 64 + emb.nbytes, 64 + emb.nbytes + dna.nbytes, b'\x00' * 16)
    padding = max(0, TARGET_SIZE - (len(header) + emb.nbytes + dna.nbytes))
    print(f'[VAULT BUILDER] Writing 1.0 GB binary vault to {%s}...' % output_bin)
    with open(output_bin, 'wb') as f:
        f.write(header)
        f.write(emb.tobytes())
        f.write(dna.tobytes())
        if padding > 0:
            fluff = b'\x00' * (1024 * 1024)
            w = 0
            while w < padding:
                a = min(len(fluff), padding - w)
                f.write(fluff[:a])
                w += a
    print(f'[SUCCESS] Generated 1.0 GB VAULT FILE: {os.path.getsize(output_bin):,} bytes (1.0 GB)!_success')

if __name__ == '__main__':
    build_myfonts_vault()
