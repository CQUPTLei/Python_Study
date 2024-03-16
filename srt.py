def extract_text_from_srt(srt_file):
    with open(srt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    subtitles = []
    current_sub = None
    for line in lines:
        line = line.strip()
        if line.isdigit():  # 判断是否为字幕序号
            if current_sub:
                subtitles.append(current_sub)
            current_sub = {'index': int(line), 'text': ''}
        elif ' --> ' in line:  # 判断是否为时间轴
            pass
        elif line == '':  # 判断是否为空行
            pass
        else:
            if current_sub:
                current_sub['text'] += line + ' '

    # 添加最后一个字幕
    if current_sub:
        subtitles.append(current_sub)

    # 提取文本
    extracted_text = ''
    for subtitle in subtitles:
        extracted_text += f"{subtitle['text']}\n"

    return extracted_text


# 用法示例
srt_file_path = 'test.srt'  # 替换成你的srt文件路径
extracted_text = extract_text_from_srt(srt_file_path)

# 输出提取到的文本
print(extracted_text)
