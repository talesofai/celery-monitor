import os


# 统一管理配置和环境变量
class Config():

    def __init__(self):
        # 初始环境变量通过K8S赋值
        self.environment = os.getenv('ENVIRONMENT', 'dev')
        print("loading environmental variables for {}".format(self.environment))

    def get_env(self, key, default=None):
        return os.getenv(key, default)

global_config = Config()
