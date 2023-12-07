## 先运行 final，后计算 speech-emotion，最后运行 final_add

### speech-emotion 的计算参考以下，并且进行了相应的修改

```bibtex
@software{speech_emotion_recognition_2019,
  author       = {Abdeladim Fadheli},
  title        = {Speech Emotion Recognition},
  version      = {1.0.0},
  year         = {2019},
  publisher    = {GitHub},
  journal      = {GitHub repository},
  url          = {https://github.com/x4nth055/emotion-recognition-using-speech}
}
```

### 主要修改了 utils.py 中的 extract_feature(file_name, **kwargs) 函数

```python
def extract_feature(file_name, **kwargs):
    """
    Extract feature from audio file `file_name`
        Features supported:
            - MFCC (mfcc)
            - Chroma (chroma)
            - MEL Spectrogram Frequency (mel)
            - Contrast (contrast)
            - Tonnetz (tonnetz)
        e.g:
        `features = extract_feature(path, mel=True, mfcc=True)`
    """
    mfcc = kwargs.get("mfcc")
    chroma = kwargs.get("chroma")
    mel = kwargs.get("mel")
    contrast = kwargs.get("contrast")
    tonnetz = kwargs.get("tonnetz")
  
    # 注释掉这一部分（对于自己没有什么作用）
    '''
    try:
        with soundfile.SoundFile(file_name) as sound_file:
            pass
    except RuntimeError:
        # not properly formated, convert to 16000 sample rate & mono channel using ffmpeg
        # get the basename
        basename = os.path.basename(file_name)
        dirname  = os.path.dirname(file_name)
        name, ext = os.path.splitext(basename)
        new_basename = f"{name}_c.wav"
        new_filename = os.path.join(dirname, new_basename)
        v = convert_audio(file_name, new_filename)
        if v:
            raise NotImplementedError("Converting the audio files failed, make sure `ffmpeg` is installed in your machine and added to PATH.")
    else:
        new_filename = file_name
    '''
    new_filename = file_name
# 修改部分

    X, sr = librosa.load(new_filename, sr=None)
    if chroma or contrast:
        stft = np.abs(librosa.stft(X))
    result = np.array([])
    if mfcc:
        mfccs = librosa.feature.mfcc(y=X, sr=sr, n_mfcc=40)       
        mfccs = np.mean(mfccs.T, axis=0) 
        result = np.hstack((result, mfccs))
    if chroma:
        chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
        chroma = np.mean(chroma.T,axis=0)
        result = np.hstack((result, chroma))
    if mel:
        mel = librosa.feature.melspectrogram(y=X, sr=sr)
        mel = np.mean(mel.T,axis=0)
        result = np.hstack((result, mel))
    if contrast:
        contrast = librosa.feature.spectral_contrast(S=stft, sr=sr)
        contrast = np.mean(contrast.T,axis=0)
        result = np.hstack((result, contrast))
    if tonnetz:
        tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sr)
        tonnetz = np.mean(tonnetz.T,axis=0)
        result = np.hstack((result, tonnetz))
    return result
```

## 注意事项

### 路径问题，代码中大部分使用绝对路径，但由于是单个处理，且为了方便，部分处理操作中直接内置了路径

### 运行顺序问题，由于路径的复用，若顺序有错不一定报错，一定要注意

### 对于上一次运行过后文件夹一定要及时清理，避免结果有误

### 文件中包含 .py 文件和 .ipynb 文件，建议使用 .ipynb 文件

## 还包含一个 alpha_and_n.ipynb 文件是为了后续快速处理其他参数，但前提是音频文件不在更换切割粒度且切割后的情感文件已经按照相应的命名要求放置在相应的位置