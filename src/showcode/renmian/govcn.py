from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    url = r'https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&searchWord=国务院任免人员&dataTypeId=15&sign=29f2fd17-e381-4e95-aa82-76ca361f7f08'
    page.goto(url)

    url_set = set()
    while True:
        page.wait_for_timeout(1000)
        links = page.query_selector_all(
            "//div/a[contains(@class, 'title log-anchor')]")
        print(f'links count is {len(links)}')
        for j in links:
            url_set.add(j.get_attribute('href'))

        next = page.get_by_role("link", name=">")
        if next.get_attribute('class') == 'next lose':
            break
        next.click()

    print(f'{len(url_set)}')
    print(f'{url_set}')

    import pickle
    from pathlib import Path

    orig_url_set = set()
    if Path('urlset.dat').exists():
        with open('urlset.dat', 'rb') as f:
            orig_url_set = pickle.load(f)
    orig_url_set = url_set - orig_url_set
    # TODO: 有空时再做 可增补更新 的任免表。

    with open('./urlset.dat', 'w+b') as f:
        pickle.dump(url_set, f)
    # df = govcn_single.renmian_df(url_set)
    # govcn_single.to_xlsx(df)
    # import pickle
    # from pathlib import Path

    # orig_url_set = set()
    # if Path('urlset.dat').exists:
    #     with open('urlset.dat', 'rb') as f:
    #         orig_url_set = pickle.load(f)
    # orig_url_set = url_set - orig_url_set

    # with open('./urlset.dat', 'w+b') as f:
    #     pickle.dump(url_set, f)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
