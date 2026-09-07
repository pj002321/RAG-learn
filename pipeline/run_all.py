from pipeline import chunk, embed, load_data, split_reviews


def run(step_name, step):
    print()
    print("=" * 60)
    print(step_name)
    print("=" * 60)
    step.main()


def main():
    run("1. 후기 분리", split_reviews)
    run("2. DB 적재", load_data)
    run("3. 청킹", chunk)
    run("4. 임베딩", embed)