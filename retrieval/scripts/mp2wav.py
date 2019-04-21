from pydub import AudioSegment ###需要安装pydub、ffmpeg
import wave
import io
#先从本地获取mp3的bytestring作为数据样本
fp=open("190421-160641.mp3",'rb')
data=fp.read()
fp.close()
#主要部分
aud=io.BytesIO(data)
sound=AudioSegment.from_file(aud,format='mp3')
raw_data = sound._data
#写入到文件，验证结果是否正确。
l=len(raw_data)
f=wave.open("123.wav",'wb')
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(16000)
f.setnframes(l)
f.writeframes(raw_data)
f.close()