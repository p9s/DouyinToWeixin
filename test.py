from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions(read_file=False)
co.use_system_user_path()
co.set_local_port(9222)
co.use_system_user_path(on_off=True)
co.set_argument('--start-maximized')
co.set_timeouts(30, 30, 30)
co.set_retry(5, 5)
co.no_imgs(on_off=True).mute(on_off=True)
page = ChromiumPage(addr_or_opts=co)

print(page.title)

page('x:/html/body/div[1]/div/div[2]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[2]/div/div[1]').input('test')
