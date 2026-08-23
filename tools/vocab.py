# -*- coding: utf-8 -*-
"""Locale vocabulary for the seed generator. LOCALE=en produces an English dataset."""
import os, random
LOCALE = os.environ.get("LOCALE", "zh")

if LOCALE == "en":
    CITIES = [("New York","NY"),("Los Angeles","CA"),("Chicago","IL"),("Houston","TX"),
              ("Seattle","WA"),("Boston","MA"),("Denver","CO"),("Atlanta","GA"),
              ("Phoenix","AZ"),("Miami","FL"),("Austin","TX"),("Portland","OR")]
    DISTRICTS = ["Downtown","Midtown","Riverside","Hillcrest","Lakeview","Old Town","Eastside","Northgate"]
    DEPTS = [(1,"Engineering"),(2,"Sales"),(3,"Marketing"),(4,"HR"),(5,"Finance"),(6,"Operations")]
    CATS  = [(1,"Electronics"),(2,"Apparel"),(3,"Groceries"),(4,"Books & Media"),
             (5,"Home & Living"),(6,"Beauty & Care")]
    CAT_BIG = {1:"Tech",2:"Fashion",3:"Food",4:"Media",5:"Home",6:"Beauty"}
    _LAST = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez",
             "Martinez","Hernandez","Lopez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson",
             "Martin","Lee","Perez","Thompson","White","Harris","Clark","Lewis","Walker","Hall"]
    _FIRST = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth",
              "William","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Chris","Karen",
              "Daniel","Nancy","Matthew","Lisa","Anthony","Betty","Mark","Sandra","Steven","Ashley"]
    def person(): return random.choice(_FIRST) + " " + random.choice(_LAST)
    STREETS = ["Main St","Oak Ave","Maple Rd","Cedar Ln","Park Blvd","Elm St","Pine Way","Lake Dr"]

    ORDER_STATUS   = ["Completed","Completed","Completed","Cancelled","Pending","Refunding"]
    PAID, UNPAID   = "Paid", "Unpaid"
    PAYM = ["Credit Card","PayPal","Bank Transfer","Apple Pay","Cash on Delivery"]
    GENDERS        = ["Male","Female"]
    USER_STATUS    = ["Active","Suspended"]
    COURSES = ["Literature","Math","English","Physics","Chemistry","History"]

    ADJ = ["Slim","Smart","HD","Portable","Wireless","Pro","Premium","Eco","Heavy-Duty",
           "Limited","Classic","Home"]
    NOUN = {1:["Bluetooth Earbuds","Power Bank","Mechanical Keyboard","Monitor","Smart Watch","Router"],
            2:["Cotton T-Shirt","Down Jacket","Running Shoes","Jeans","Summer Dress","Baseball Cap"],
            3:["Organic Rice","Cold Brew Coffee","Nut Gift Box","Milk Powder","Live Crab","Olive Oil"],
            4:["Database System Concepts","Introduction to Algorithms","Vinyl Record",
               "Sci-Fi Anthology","Picture Book","Photography Album"],
            5:["Storage Bin","Latex Pillow","Stainless Wok","Humidifier","Bedding Set","Drying Rack"],
            6:["Face Serum","Cleanser","Lipstick","Sunscreen","Sheet Mask Set","Perfume"]}
    LONG_SUFFIX = ["2026 Flagship Edition Official Warranty Included",
                   "Family Value Pack Free Shipping Guaranteed Authentic",
                   "Limited Gift Box With Custom Engraving Service",
                   "Bestselling Classic With 7-Day Free Returns"]
    SHOP_ADJ = ["Prime","Choice","Swift","Joy","Craft","Cloud"]
    SHOP_KIND = ["Flagship Store","Specialty Store","Official Store"]
    REVIEW_TEXT = ["Fast shipping, good quality","Just okay","Very satisfied, will buy again",
                   "Not as described","Package arrived damaged","Great value, recommended"]
    COMMENT_SHORT = ["Nicely written!","Learned a lot","Is this a typo?","Bookmarked","Thanks for sharing"]
    COMMENT_LONG = ("This article explains the evaluation order of window functions really clearly, "
        "especially the difference between the default RANGE frame and an explicit ROWS frame. I had "
        "misunderstood it for a long time, which caused our running totals to double-count whenever a "
        "single day had more than one order. After reading it I rewrote every cumulative-sum query to "
        "use ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW and the problem disappeared. The point "
        "about LAST_VALUE needing an explicit UNBOUNDED FOLLOWING frame is just as important. I hope "
        "the author writes a follow-up on recursive CTEs.")
    ARTICLE_TOPIC = ["Indexes","Transactions","Window Functions","Execution Plans","Partitioned Tables"]
    ARTICLE_FMT = "Understanding {} in Depth ({})"
    TAGS = ["mysql","sql","window-functions","indexing","tuning","postgres",
            "data-warehouse","hive","clickhouse","partitioning"]
    TICKET_SUBJECTS = ["Cannot sign in","Refund status","Invoice request","Delivery delayed","Coupon not working"]
    BLACKLIST_REASONS = ["Order brushing","Abusive returns","Payment fraud"]
    VIDEO_TITLE = "SQL in Practice, Episode {}"
    ROLLUP_SMALL = "— subtotal —"
    ROLLUP_BIG   = "— all categories —"
else:
    CITIES = [("北京","北京市"),("上海","上海市"),("广州","广东省"),("深圳","广东省"),
              ("杭州","浙江省"),("成都","四川省"),("武汉","湖北省"),("南京","江苏省"),
              ("西安","陕西省"),("重庆","重庆市"),("苏州","江苏省"),("天津","天津市")]
    DISTRICTS = ["朝阳区","海淀区","浦东新区","天河区","西湖区","武侯区","江汉区","鼓楼区"]
    DEPTS = [(1,"技术部"),(2,"销售部"),(3,"市场部"),(4,"人事部"),(5,"财务部"),(6,"运营部")]
    CATS  = [(1,"电子产品"),(2,"服装鞋帽"),(3,"食品生鲜"),(4,"图书音像"),(5,"家居日用"),(6,"美妆个护")]
    CAT_BIG = {1:"数码",2:"服饰",3:"食品",4:"文娱",5:"家居",6:"美妆"}
    _SURNAMES = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
    _GIVEN = ["伟","芳","娜","敏","静","丽","强","磊","洋","艳","勇","军","杰","娟","涛","明","超","秀英","霞","平"]
    def person(): return random.choice(_SURNAMES) + random.choice(_GIVEN)
    STREETS = ["科技路","人民路","解放路","中山路","建设路"]

    ORDER_STATUS   = ["已完成","已完成","已完成","已取消","待发货","退款中"]
    PAID, UNPAID   = "已支付", "未支付"
    PAYM = ["支付宝","微信支付","银行卡","云闪付","货到付款"]
    GENDERS        = ["男","女"]
    USER_STATUS    = ["正常","禁用"]
    COURSES = ["语文","数学","英语","物理","化学","历史"]

    ADJ = ["超薄","智能","高清","便携","无线","专业","轻奢","环保","加厚","限量版","经典","家用"]
    NOUN = {1:["蓝牙耳机","移动电源","机械键盘","显示器","智能手表","路由器"],
            2:["纯棉T恤","羽绒服","运动鞋","牛仔裤","连衣裙","棒球帽"],
            3:["有机大米","冷萃咖啡","坚果礼盒","新西兰奶粉","阳澄湖大闸蟹","初榨橄榄油"],
            4:["数据库系统概念","算法导论","黑胶唱片","科幻小说集","儿童绘本","摄影画册"],
            5:["收纳箱","乳胶枕","不锈钢炒锅","加湿器","四件套床品","折叠晾衣架"],
            6:["精华液","洗面奶","口红","防晒霜","面膜礼盒","香水"]}
    LONG_SUFFIX = ["2026 旗舰款 官方正品 全国联保","家庭超值装 顺丰包邮 假一赔十",
                   "限量礼盒装 含专属定制刻字服务","畅销经典款 支持七天无理由退换"]
    SHOP_ADJ = ["优选","臻品","速达","乐购","匠心","云端"]
    SHOP_KIND = ["旗舰店","专营店","自营店"]
    REVIEW_TEXT = ["物流很快，质量不错","一般般吧","非常满意，还会回购","和描述不符","包装破损","性价比高，推荐"]
    COMMENT_SHORT = ["写得好！","学到了","这里是不是有误？","收藏了","感谢分享"]
    COMMENT_LONG = ("这篇文章把窗口函数的执行顺序讲得非常透彻，特别是关于默认窗口框架 RANGE 与 ROWS 的差异部分，"
        "我之前一直理解错了，导致线上报表的累计值在同一天有多笔订单时出现了重复累加的问题。看完之后我回去把所有"
        "累计求和的 SQL 都改成了显式 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW，问题就解决了。"
        "另外关于 LAST_VALUE 需要显式扩展窗口到 UNBOUNDED FOLLOWING 这一点也非常关键，"
        "希望作者以后能再写一篇关于递归 CTE 的深度文章。")
    ARTICLE_TOPIC = ["索引","事务","窗口函数","执行计划","分区表"]
    ARTICLE_FMT = "深入理解{}（{}）"
    TAGS = ["mysql","sql","窗口函数","索引","调优","postgres","数据仓库","hive","clickhouse","分区"]
    TICKET_SUBJECTS = ["无法登录","退款进度","发票申请","物流延迟","优惠券失效"]
    BLACKLIST_REASONS = ["刷单","恶意退货","支付欺诈"]
    VIDEO_TITLE = "SQL 实战第 {} 讲"
    ROLLUP_SMALL = "— 小类合计 —"
    ROLLUP_BIG   = "— 所有大类 —"
