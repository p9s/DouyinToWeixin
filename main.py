import datetime
import time
import os
from DrissionPage import ChromiumPage, ChromiumOptions


def print_msg(msg):
    print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}')


def init_page_and_tabs():
    co = ChromiumOptions(read_file=False)
    co.use_system_user_path()
    co.set_local_port(9222)
    co.use_system_user_path(on_off=True)
    co.set_argument('--start-maximized')
    co.set_timeouts(30, 30, 30)
    co.set_retry(5, 5)
    co.no_imgs(on_off=True).mute(on_off=True)
    p = ChromiumPage(addr_or_opts=co)

    tab_1 = None
    tab_1_id = p.find_tabs(url='douyin.com')
    if tab_1_id:
        tab_1 = p.get_tab(tab_1_id)
    else:
        tab_1 = p.new_tab('https://www.douyin.com/')

    tab_2 = None
    tab_2_id = p.find_tabs(url='weixin.qq.com')
    if tab_2_id:
        tab_2 = p.get_tab(tab_2_id)
    else:
        tab_2 = p.new_tab('https://channels.weixin.qq.com/platform')

    return p, tab_1, tab_2


def post_video(aweme_id, desc):
    print_msg('正在上传视频：' + aweme_id + '.mp4')
    tab_weixin.get('https://channels.weixin.qq.com/platform')
    tab_weixin.wait(5)
    tab_weixin('tag:button@text()=发表视频').click()
    tab_weixin.wait(5)
    tab_weixin('tag:input@type=file').input(os.path.join(os.getcwd(), 'video', aweme_id + ".mp4"))
    tab_weixin.wait(2)
    tab_weixin('x:/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[2]/div/div[1]').input(desc)
    tab_weixin.wait(2)
    tab_weixin('.post-position-wrap').click()
    tab_weixin.wait(2)
    tab_weixin('不显示位置').click()
    tab_weixin.wait(2)
    # tab_weixin('作品将展示原创标记').click()
    # tab_weixin.wait(2)
    # tab_weixin('x:/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/div[9]/div[3]/div[1]/div/div[2]/div/div[3]/label').click()
    # tab_weixin.wait(2)
    # tab_weixin('x:/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/div[9]/div[3]/div[1]/div/div[3]/div[2]').click()
    # tab_weixin.wait(2)
    tab_weixin.wait.ele_displayed('x:/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[1]/div[2]/div/div[2]/div/span/div/div/div')
    tab_weixin.wait(2)
    tab_weixin.scroll.to_bottom()
    tab_weixin.wait(2)
    tab_weixin('tag:button@text()=发表').click()
    tab_weixin.wait(2)
    print_msg(aweme_id + '.mp4' + "上传成功")


def loop_function():
    tab_douyin.listen.start('www.douyin.com/aweme/v1/web/aweme/post')
    tab_douyin.refresh()
    res = tab_douyin.listen.wait(timeout=30)
    tab_douyin.listen.stop()
    if res:
        if not res.is_failed:
            if isinstance(res.response.body, dict):
                try:
                    aweme_list = res.response.body["aweme_list"]
                    for dic in aweme_list:
                        create_time = dic['create_time']
                        aweme_id = dic['aweme_id']
                        media_type = dic['media_type']
                        # create_time > start_time, aweme_id not in posted_list, media_type  == 4
                        if create_time > start_time and aweme_id not in posted_list and media_type == 4:
                            # 获取视频链接，并下载
                            video_url = dic['video']['play_addr']['url_list'][0]
                            path = os.path.join(os.getcwd(), "video")
                            d_r = tab_douyin.download(file_url=video_url, rename=aweme_id, suffix='mp4', goal_path=path,
                                                      file_exists='overwrite')
                            if d_r[0] == 'success':
                                # 调用发布函数
                                desc = dic['desc']
                                post_video(aweme_id, desc)
                                posted_list.append(aweme_id)
                            else:
                                print_msg('下载视频失败')
                except KeyError:
                    print_msg("The key 'aweme_list' does not exist in the dictionary")
            else:
                print_msg("The response body is not a dictionary")
        else:
            print_msg("Failed to get response")
    else:
        print_msg("Waited for 30 seconds but no response was received")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    page, tab_douyin, tab_weixin = init_page_and_tabs()
    tab_weixin.set.auto_handle_alert()
    start_time = int(time.time())
    posted_list = []

    index = 1
    while True:
        print_msg(f'第{index}次检查~')
        index += 1
        loop_function()
        time.sleep(60)

        if (int(time.time()) - start_time) % 3000 <= 60:
            tab_weixin.refresh()
