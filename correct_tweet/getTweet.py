import os
import tweepy
import datetime
import mysql.connector
from dotenv import load_dotenv
load_dotenv(override=True)

mysql_id = os.getenv('MYSQL_ID')
mysql_password = os.getenv('MYSQL_PASSWORD')

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_secret = os.getenv('ACCESS_SECRET')


def insert_to_db(img_name, hashtag, binary_data):
    cnx = None

    try:
        cnx = mysql.connector.connect(
            user= mysql_id,  # ユーザー名
            password= mysql_password,  # パスワード
            host='localhost',  # ホスト名(IPアドレス）
            database='sampledb'  # データベース名
        )

        print(cnx.is_connected())
    
        cursor=cnx.cursor()

        cnx.commit()

        sql = ('''INSERT INTO img_to_binary (name, hashtag, img) VALUES (%s, %s, %s)''')

    
        cursor.execute(sql, (img_name, hashtag, binary_data))
    
        cnx.commit()

        print(f"{cursor.rowcount} records inserted.")

        cursor.close()
    except Exception as e:
        print(f"Error Occurred: {e}")

    finally:
        if cnx is not None and cnx.is_connected():
            cnx.close()

def gettwitterdata(keyword,dfile):

    #認証
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit = True)

    #検索キーワード設定 
    q = keyword

    #つぶやきを格納するリスト
    tweets_data =[]

    #カーソルを使用してデータ取得
    for tweet in tweepy.Cursor(api.search_tweets, q=q, count=10, tweet_mode='extended').items(10):

        #つぶやき時間がUTCのため、JSTに変換  ※デバック用のコード
        #jsttime = tweet.created_at + datetime.timedelta(hours=9)
        #print(jsttime)

        #つぶやきテキスト(FULL)を取得
        tweets_data.append(tweet.full_text + '\n')


    #出力ファイル名
    fname = r"'"+ dfile + "'"
    fname = fname.replace("'","")

    #ファイル出力
    with open(fname, "w",encoding="utf-8") as f:
        f.writelines(tweets_data)


if __name__ == '__main__':

    #検索キーワードを入力  ※リツイートを除外する場合 「キーワード -RT 」と入力
    print ('====== Enter Serch KeyWord   =====')
    keyword = input('>  ')

    #出力ファイル名を入力(相対パス or 絶対パス)
    print ('====== Enter Tweet Data file =====')
    dfile = input('>  ')

    gettwitterdata(keyword,dfile)