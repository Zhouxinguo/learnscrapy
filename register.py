
import requests


def register():
    url = 'https://antispider7.scrape.center/api/register'
    # 简单设置账号密码邮箱为同一个值
    for a in range(20):
        d = f'12345{a}'
        data = {
            'username': d,
            'password': d,
        }
        r = requests.post(url=url, data=data)
        print(f'12345{a}-{r.status_code}')


if __name__ == '__main__':
    register()