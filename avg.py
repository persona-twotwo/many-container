import os
import argparse

def calculate_average(file_path, n, m):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 필요한 줄 선택 (뒤에서 n줄, 마지막 m줄 제외)
    selected_lines = lines[-n:-m] if m > 0 else lines[-n:]
    
    total = 0
    count = 0
    for line in selected_lines:
        try:
            # 두 번째 컬럼(인덱스 1)의 값을 추출
            value = float(line.split()[1])
            total += value
            count += 1
        except (IndexError, ValueError):
            # 잘못된 형식의 줄은 무시
            continue
    
    return total / count if count > 0 else 0

def process_log_files(directory, n, m):
    results = {}
    for filename in os.listdir(directory):
        if filename.endswith('.out'):
#        if filename.endswith('.log'):
            file_path = os.path.join(directory, filename)
            avg = calculate_average(file_path, n, m)
            results[filename] = avg
    return results

def main():
    parser = argparse.ArgumentParser(description='Calculate average from log files.')
    parser.add_argument('directory', help='Directory containing log files')
    parser.add_argument('n', type=int, help='Number of lines to consider from the end')
    parser.add_argument('m', type=int, help='Number of lines to exclude from the end')
    args = parser.parse_args()

    results = process_log_files(args.directory, args.n, args.m)

    for filename, avg in results.items():
        print(f"{filename}: {avg:.6f}")

    all_avg = 0
    for _, avg in results.items():
        all_avg += avg

    print(f"all avg: {all_avg / len(results)}")

if __name__ == "__main__":
    main()
