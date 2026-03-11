

cs = on_startswith({"土豆", "今日土豆", "🥔"}, priority=1, block=True)


@cs.handle()
async def _handle(bot: Bot, event: MessageEvent):
    if event.user_id == 951602078:
        raise exception.FinishedException
    msg = str(event.message)
    if msg[:2] == "土豆":
        try:
            n = int(msg[2:])
            if 1 <= n <= 2177:
                await cs.send(image_(ptt / (str(n) + ".gif")))
            else:
                i = random.randint(1, 2177)
                await cs.send(
                    "随机土豆（" + str(i) + "/2177）\n🌈发【土豆x】直接出x号土豆"
                )
                await cs.send(image_(ptt / (str(i) + ".gif")))
        except:
            i = random.randint(1, 2177)
            await cs.send("随机土豆（" + str(i) + "/2177）\n🌈发【土豆x】直接出x号土豆")
            await cs.send(image_(ptt / (str(i) + ".gif")))
    elif msg[:1] == "🥔":
        try:
            n = int(msg[1:])
            if 1 <= n <= 2177:
                await cs.send(image_(ptt / (str(n) + ".gif")))
            else:
                i = random.randint(1, 2177)
                await cs.send(
                    "随机土豆（" + str(i) + "/2177）\n🌈发【土豆x】直接出x号土豆"
                )
                await cs.send(image_(ptt / (str(i) + ".gif")))
        except:
            i = random.randint(1, 2177)
            await cs.send("随机土豆（" + str(i) + "/2177）\n🌈发【土豆x】直接出x号土豆")
            await cs.send(image_(ptt / (str(i) + ".gif")))
    else:
        i = random.randint(1, 2177)
        await cs.send("随机土豆（" + str(i) + "/2177）\n🌈发【土豆x】直接出x号土豆")
        await cs.send(image_(ptt / (str(i) + ".gif")))
