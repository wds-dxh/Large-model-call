from zhipuai import ZhipuAI

client = ZhipuAI(api_key="334f9bba3a40a758ae8586464a77698a.QCIwFck36K2xVGYN") # 请填写您自己的APIKey

job = client.fine_tuning.jobs.create(
    model="chatglm_130b",
    training_file="test.json",   # 请填写已成功上传的文件id
    validation_file="test.json", # 请填写已成功上传的文件id
    suffix="<self-defined>",
)
job_id = job.id

print(job_id)