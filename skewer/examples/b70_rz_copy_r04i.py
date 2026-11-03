from pathlib import Path
import ast,struct,numpy as np
source=Path("experiments/parity-b70-s157-native-r01-20260915/native/s157_final_blend.py")
tree=ast.parse(source.read_text(encoding="utf-8"))
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)
        and n.name=="f32_to_f16_round_toward_zero")
env={"np":np}
exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source),"exec"),env)
x=np.array([0.5004,0.9999,-0.0,1.0],dtype=np.float32)
rne=x.astype(np.float16)
rz=env["f32_to_f16_round_toward_zero"](x)
for a,b,c in zip(x,rne,rz):
 print("F32",float(a),"RN16",float(b),f"0x{int(b.view(np.uint16)):04x}",
       "RZ16",float(c),f"0x{int(c.view(np.uint16)):04x}")
# Synthetic already-published RGBA16F bytes; source / destination padding differ.
width,height=2,2
src_pitch,dst_pitch=20,24
src=bytearray([0xcc])*(src_pitch*height)
dst=bytearray([0xa5])*(dst_pitch*height)
pixel=struct.pack("<4H",0x3800,0x3400,0x0000,0x3c00)
for row in range(height):
 src[row*src_pitch:row*src_pitch+width*8]=pixel*width
 dst[row*dst_pitch:row*dst_pitch+width*8]=src[row*src_pitch:row*src_pitch+width*8]
assert all(dst[y*dst_pitch:y*dst_pitch+width*8]
           ==src[y*src_pitch:y*src_pitch+width*8] for y in range(height))
assert all(dst[y*dst_pitch+width*8:(y+1)*dst_pitch]
           ==bytes([0xa5])*(dst_pitch-width*8) for y in range(height))
print("history_payload_byte_equal",width*height*8,"destination_padding_preserved",True)
