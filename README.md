Welcome to Group 1 Repository.
This project attempts to improve the code clone detection by incorporating AST in the fine-tuning stage, not only pretraining like the original UniXcoder research did.

This repo provides the code for reproducing the experiments in [CodeBERT: A Pre-Trained Model for Programming and Natural Languages](https://arxiv.org/pdf/2002.08155.pdf). CodeBERT is a pre-trained model for programming language, which is a multi-programming-lingual model pre-trained on NL-PL pairs in 6 programming languages (Python, Java, JavaScript, PHP, Ruby, Go).

# Local Set up 

First, you should clone this repository. 
Before installing libraries, we highly recommend to set up the requirements in a virtual environment of your own choice.

In case you use mac or linux, the path we set using double backslash might not work. Please adjust to your own OS.

In 'docker' branch, the paths are already adjusted for linux and macos. 

Paths are in 
1. UniXcoder/downstream-tasks/clone-detection/POJ-104/dataset/preprocess.py
2. UniXcoder/downstream-tasks/clone-detection/POJ-104/preprocess.py
3. UniXcoder/downstream-tasks/clone-detection/POJ-104/run.py
4. GraphCodeBERT/clonedetection/run.py
5. GraphCodeBERT/clonedetection/preprocess.py

Beside these files, if you notice any path error, please adjust those as well.

## Dependency
- pip install torch
- pip install transformers
- pip install -U scikit-learn
- pip install tree-sitter (If you do not have a C-compiler, you will get an error. Please follow the solution mentioned in the error. )
- pip install gdown

You can choose to simply install with requirements.txt.
```
pip install -r requirements.txt
```

## Torch
If you have a fancy gpu that can run torch with cuda, go ahead and install cuda version!
[Torch-Website](https://pytorch.org/) gives you a command for you. 
Make sure that you have installed CudaToolkit and the versions between torch cuda and your CudaToolkit matches.

It is not mandatory to have GPU to run our code. Using Cuda is your choice.

## Tree-Sitter
In order to get the full AST, Tree-Sitter library is used.
Please run both build.sh in TreeSitter/ and GraphCodeBERT/clonedetection/parserX/. These will clone the tree-sitter repositories.

However, if it does not work for you somehow, then you can manually download the repository and change the path like the following:
First, clone the repository from [tree-sitter-cpp](https://github.com/tree-sitter/tree-sitter-cpp) and Parser_X(GraphCodeBERT/clonedetection/parserX/build.sh)/ [tree-sitter-java](https://github.com/tree-sitter/tree-sitter-java).
You can set your own path inside Language.build_library() in preprocess() function in model_name/downstream-tasks/clone-detection/POJ-104/preprocess.py.

As this library is not build only with python, C-compiler is necessary. 
This can be different per os version, and the choice is up to you.
For Windows user, installing visual studio can be a solution by looking at this website [microsoft guide](https://devblogs.microsoft.com/cppblog/getting-started-with-visual-studio-for-c-and-cpp-development/#Setup).
Or the error while installing tree-sitter can perfectly guide you to resolve the issue.

## UniXcoder Dataset

Download and Preprocess [Instruction Guide](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Code/Clone-detection-POJ-104)

1.Download dataset from website or run the following command:
```
cd dataset
pip install gdown
gdown https://drive.google.com/u/0/uc?id=19cH5Tkk38OJmEqAObr3pLmUj76oLqSoW
tar -xvf programs.tar.gz
cd ..
```
In case you get a Permission related error, please manually download the google drive via the link.

2.Preprocess data

```
cd dataset
python preprocess.py
cd ..
```

## GraphCodeBERT Dataset

For GraphCodeBERT, the dataset is already placed in the GraphCodeBERT/clonedetection/dataset, so no additional download or preprocessing is required.

# Option: Docker
In Docker branch, you can run evaluation with Docker.

Check out the 'Optional: Docker Setup' of the README in Docker Branch.


# How to Fine-Tune?

## How to choose mode: Simplified AST, Full AST, code or both?

convert_examples_to_features() in run.py should be adjusted to select certain mode.

Update the argument of extract_dataflow() for GraphCodeBERT.

Update the argument of tokenizer.tokenize() for UniXcoder.

1. Running with Simplified AST
```
Preprocess().preprocess(func, Mode.SIMPLIFIED)
```

2. Running with Full AST

```
Preprocess().preprocess(func, Mode.FULL)
```

3. UniXcoder: Running with AST and code 

```
code_tokens = tokenizer.tokenize(code+Preprocess().preprocess(code, Mode.SIMPLIFIED))[:args.block_size-4]
```

4. GraphCodeBERT: Running with AST and code

```
code_tokens,dfg=extract_dataflow(func+Preprocess().preprocess(func, Mode.SIMPLIFIED),parser,'java')
```

## UniXcoder
This repo will provide the code for improving the code clone detection in [UniXcoder: Unified Cross-Modal Pre-training for Code Representation](https://arxiv.org/pdf/2203.03850.pdf). UniXcoder is a unified cross-modal pre-trained model for programming languages to support both code-related understanding and generation tasks. 

Please refer to the [UniXcoder](https://github.com/microsoft/CodeBERT/tree/master/UniXcoder) folder for tutorials and downstream tasks.

Please check the README in UniXcoder before you start running them.

We have fine-tuned UniXcoder using the following pretrained model [link](https://huggingface.co/microsoft/unixcoder-base). 

### How to train Clone Detection with UniXcoder?

1. Go to POJ-104 under clone-detection of UniXcoder.
2. We recommend the following code snippet to run the run.py.

```
python run.py
--output_dir saved_models
--model_name_or_path microsoft/unixcoder-base
--do_train --train_data_file dataset/train.jsonl
--eval_data_file dataset/valid.jsonl
--test_data_file dataset/test.jsonl
--num_train_epochs 2 --block_size 350
--train_batch_size 4 --eval_batch_size 8
--learning_rate 2e-5 --max_grad_norm 1.0
--seed 123456 
```

## GraphCodeBERT

This repo also provides the code for reproducing the experiments in [GraphCodeBERT: Pre-training Code Representations with Data Flow](https://openreview.net/pdf?id=jLoC4ez43PZ). GraphCodeBERT is a pre-trained model for programming language that considers the inherent structure of code i.e. data flow, which is a multi-programming-lingual model pre-trained on NL-PL pairs in 6 programming languages (Python, Java, JavaScript, PHP, Ruby, Go). 

For downstream tasks like code search, clone detection, code refinement and code translation, please refer to the [GraphCodeBERT](https://github.com/guoday/CodeBERT/tree/master/GraphCodeBERT) folder.

Please check the README in GraphCodeBERT before you start running them.

We have fine-tuned GraphCodeBERT using the following pretrained model [link](https://huggingface.co/microsoft/graphcodebert-base).

### How to train Clone Detection with GraphCodeBERT?

1. Go to run.py under GraphCodeBERT/clonedetection.
3. We recommend the following code snippet to run the run.py
```
python run.py
--output_dir=saved_models
--config_name=microsoft/graphcodebert-base
--model_name_or_path=microsoft/graphcodebert-base
--tokenizer_name=microsoft/graphcodebert-base
--do_train --train_data_file=dataset/train.txt
--eval_data_file=dataset/valid.txt
--test_data_file=dataset/test.txt
--epoch 1
--code_length 256
--data_flow_length 64
--train_batch_size 4
--eval_batch_size 32
--learning_rate 2e-5
--max_grad_norm 1.0
--evaluate_during_training
--seed 123456 2>&1| tee saved_models/train.log
```


# Fine-tuned model & Inference

Our fine-tuned model can be found in [UniXcoder-simplified-AST](https://drive.google.com/file/d/1pQWHLmJaBs9u3K0Q6Av_lYev_CGvTOk7/view). 

This model is the fine-tuned UniXcoder with only simplified AST, meaning no code, no variable name.

You can also simply download the fine-tuned model via the following command.

Please follow the command inside POJ-104.

```
mkdir saved_models\checkpoint-best-map
cd saved_models\checkpoint-best-map
pip install gdown
gdown https://drive.google.com/u/0/uc?id=1vs7M3gYLcWSnVvfIxI6i1eleHXS3Sd9-
```

Make sure to place the downloaded fine-tuned model under UniXcoder/downstream-tasks/clone-detection/POJ-104/saved_models/checkpoint-best-map.

## How can we use the model for inference?

If you are using CPU, then replace line 350 in run.py of UniXcoder with the following command.
```
model_to_load.load_state_dict(torch.load(output_dir), map_location=torch.device('cpu'))  
```

Run the command below in POJ-104.

```
python run.py 
--output_dir saved_models 
--model_name_or_path microsoft/unixcoder-base 
--do_eval 
--eval_data_file dataset/valid.jsonl 
--test_data_file dataset/test.jsonl 
--block_size 350 
--eval_batch_size 4 
--learning_rate 2e-5 
--max_grad_norm 1.0 
--seed 123456
```

## Results

Here is the result that you can obtain with our fine-tuned model and also the original UniXcoder result.
The interpretation can be found in our report.

| Model                         | mAP    |
|-------------------------------|--------|
| Original UniXcoder Reference  | 0.9052 |
| UniXcoder with Simplified AST | 0.5806 |

## Contact
Feel free to contact Group 1 via MatterMost if there is any question! Might be able to help you in terms of set up :)

(Daan Hofman, Pascal Benschop, Jeongwoo Park, Leon Kempen, Aron Bevelander)
