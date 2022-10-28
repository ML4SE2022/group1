FROM python:3.10

# Install the latest gcc (should be version 10)
RUN apt-get install -y gcc

COPY requirements.txt requirements.txt
COPY UniXcoder/downstream-tasks/clone-detection/POJ-104/ /POJ-104/
COPY TreeSitter/ /TreeSitter/

RUN pip3 install -r requirements.txt

WORKDIR /TreeSitter
RUN sh build.sh

WORKDIR /POJ-104/dataset
RUN sh download.sh

WORKDIR /POJ-104
RUN sh model_script.sh

CMD ["python", "run.py", \
"--output_dir", "saved_models", \
"--model_name_or_path", "microsoft/unixcoder-base", \
"--do_eval", \
"--eval_data_file", "dataset/valid.jsonl", \
"--test_data_file", "dataset/test.jsonl", \
"--block_size", "350", \
"--eval_batch_size", "4", \
"--learning_rate", "2e-5", \
"--max_grad_norm", "1.0", \
"--seed", "123456"]
