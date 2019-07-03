import json
import jmespath
from utils.client import HTTPClient

# 完成了对JSON格式的抽取器，如果返回结果是JSON串，我们可以通过这个抽取器找到我们想要的数据，再进行下一步的操作，或者用来做断言。
class JMESPathExtractor(object):
    """
    用JMESPath实现的抽取器，对于json格式数据实现简单方式的抽取。
    """
    def extract(self, query=None, body=None):
        try:
            return jmespath.search(query, json.loads(body))
        except Exception as e:
            raise ValueError("Invalid query: " + query + " : " + str(e))


if __name__ == '__main__':
