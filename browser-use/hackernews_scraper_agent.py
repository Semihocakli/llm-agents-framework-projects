from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
import json

async def hackernews_scraper():
    task = '''Hacker News "Show HN" sayfasına git ve ilk 5 gönderiyi çek:
    1. Gönderi başlıklarını al
    2. Gönderi URL'lerini çıkar
    3. Yorum sayılarını bul
    4. Gönderi saatini kontrol et (saat cinsinden)'''

    model = ChatOpenAI(model='gpt-4o')
    agent = Agent(task=task, llm=model)

    try:
        history = await agent.run()
        result = history.final_result()

        if result:

            data = json.loads(result)
            for idx, post in enumerate(data.get("posts", []), 1):
                print(f"\n Gönderi {idx}:")
                print(f"Başlık: {post.get('post_title', 'Bilgi yok')}")
                print(f"URL: {post.get('post_url', 'Bilgi yok')}")
                print(f"Yorum Sayısı: {post.get('num_comments', 0)}")
                print(f"Yayınlanma Süresi: {post.get('hours_since_post', 0)} saat")
        else:
            print(" Sonuç alınamadı.")

    except Exception as e:
        print(f" Hata: {str(e)}")


if __name__ == '__main__':
    asyncio.run(hackernews_scraper())