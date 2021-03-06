
import requests


def register():
    url = 'https://antispider6.scrape.center/register'
    # 简单设置账号密码邮箱为同一个值
    for a in range(100):
        d = f'1234-{a}@qq.com'
        data = {
            'username': d,
            'email': d,
            'password1': d,
            'password2': d
        }
        r = requests.post(url=url, data=data)
        print(f'1234-{a}@qq.com-{r.status_code}')


if __name__ == '__main__':
    register()