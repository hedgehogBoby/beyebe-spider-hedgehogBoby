import re

if __name__ == '__main__':
    string = '<div class=\"summary\">\n\t\t\t\t\t故事发生在偏僻贫瘠的山村之中。张保民（宋洋 饰）是一名矿工，一天，他被妻子翠霞（谭卓 饰）叫回了家，原来，他们的儿子失踪了。带着儿子的照片，不会说话的张保民踏上了寻子之路，途中，他遇见了大资本家昌万年（姜武 饰）的爪牙，两方人马起了冲突，昌万年骗张保民自己知道他儿子的下落，实际上，他隐藏了一个黑暗的秘密。昌万年一直靠着行贿非法收购煤矿以牟取暴利，身为他的律师，徐文杰知道了太多不可告人的秘密。公检法机构开始着手调查昌万年的公司，徐文杰在这个节骨眼上玩起了失踪。为了逼迫徐文杰就范，昌万年绑架了他的女儿。\n\t\t\t\t\t</div>'.replace(
        '\n', '').replace('\t', '')
    pattern = """<div class="summary">(.*?)</div>"""
    matchObj = re.search(pattern, string, flags=0)
    if matchObj is not None:
        print(matchObj.group(0))
        print(matchObj.group(1))


