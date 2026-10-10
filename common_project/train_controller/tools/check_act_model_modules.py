from lerobot.policies.act import ACTPolicy

target_model_repo_id = "Iwas-6127/act-model-mypick-color-20260926_235331"

policy = ACTPolicy.from_pretrained(target_model_repo_id)

for name, module in policy.named_modules():
    print(name)