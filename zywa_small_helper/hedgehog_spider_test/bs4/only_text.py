str = """<div id="info">
        <span><span class="pl">导演</span>: <span class="attrs"><a href="/celebrity/1103667/" rel="v:directedBy">李沧东</a></span></span><br>
        <span><span class="pl">编剧</span>: <span class="attrs"><a href="/celebrity/1103667/">李沧东</a> / <a href="/celebrity/1393365/">吴正美</a> / <a href="/celebrity/1014497/">村上春树</a></span></span><br>
        <span class="actor"><span class="pl">主演</span>: <span class="attrs"><span><a href="/celebrity/1246859/" rel="v:starring">刘亚仁</a> / </span><span><a href="/celebrity/1275960/" rel="v:starring">史蒂文·元</a> / </span><span><a href="/celebrity/1382416/" rel="v:starring">全钟瑞</a> / </span><span><a href="/celebrity/1388997/" rel="v:starring">金秀京</a> / </span><span><a href="/celebrity/1378205/" rel="v:starring">崔承浩</a> / </span><span style="display: inline;"><a href="/celebrity/1383972/" rel="v:starring">玉子妍</a></span><a href="javascript:;" class="more-actor" title="更多主演" style="display: none;">更多...</a></span></span><br>
        <span class="pl">类型:</span> <span property="v:genre">剧情</span> / <span property="v:genre">悬疑</span><br>
        p
        <span class="pl">制片国家/地区:</span> 韩国<br>
        <span class="pl">语言:</span> 韩语<br>
        <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2018-05-16(戛纳电影节)">2018-05-16(戛纳电影节)</span> / <span property="v:initialReleaseDate" content="2018-05-17(韩国)">2018-05-17(韩国)</span><br>
        <span class="pl">片长:</span> <span property="v:runtime" content="148">148分钟</span><br>
        <span class="pl">又名:</span> 燃烧烈爱(台) / Burning / Beoning<br>
        <span class="pl">IMDb链接:</span> <a href="http://www.imdb.com/title/tt7282468" target="_blank" rel="nofollow">tt7282468</a><br>

</div>"""
from bs4 import BeautifulSoup

soup = BeautifulSoup(str, "html.parser")
print(soup.text)
