import datetime
import pandas_datareader.data as pdr
import smtplib
from email.message import EmailMessage
from pandas_datareader._utils import RemoteDataError

# Creating base trend follower class
class TrendFollower:
    def __init__(self, user_name, user_password, email_name, email_password):
        self.user_name = user_name
        self.user_password = user_password
        self.email_name = email_name
        self.email_password = email_password
        self.data = {self.user_name: {'password': self.user_password}}
        self.markets_data = [{'name':'S&P 500'}, {'name':'GOLD'}, {'name':'BITCOIN'}]
        self.marketspro_data = [{'name':'S&P 500'}, {'name':'NASDAQ'}, {'name':'DOW JONES'}, 
            {'name':'NIKKEI'}, {'name':'GOLD'}, {'name':'SILVER'}, {'name':'BITCOIN'}, {'name':'LITECOIN'}, 
            {'name':'ETHEREUM'}, {'name':'US DOLLAR'}, {'name':'JP YEN'}, {'name':'CH FRANC'}, {'name':'CA DOLLAR'}]
        self.markets = {
            'S&P 500' : 'SP500',
            'DOW JONES' : 'DJIA',
            'NASDAQ' : 'NASDAQ100',
            'NIKKEI' : 'NIKKEI225',
            'GOLD' : 'GOLDAMGBD228NLBM',
            'SILVER' : 'SLVPRUSD',
            'US DOLLAR' : 'DTWEXBGS',
            'JP YEN' : 'DEXJPUS',
            'CH FRANC' : 'DEXSZUS',
            'CA DOLLAR' : 'DEXCAUS',
            'BITCOIN' : 'CBBTCUSD',
            'LITECOIN' : 'CBLTCUSD',
            'ETHEREUM' : 'CBETHUSD'
            }  
    
    # Fetching data from Federal Reserve API and establishing current trend direction
    def get_trend(self, symbol, start = datetime.datetime(2020, 1, 1), end = datetime.datetime.now()):
        try:
            df = pdr.DataReader(symbol, 'fred', start, end)
            if df[symbol][-1] > df[symbol][-252]:
                return 'BULLISH'
            else:
                return 'BEARISH'
        except RemoteDataError:
            return 'CONNECTION ERROR.'
    
    # Sending email using gmail and smtplib
    def send_mail(self, name, email):
        message = "Thank you" + " " + name.capitalize() + " " + "for registration. You can now login with the Trend Follower - name:" + " " + self.user_name + "and password:" + " " + self.user_password + "."
        msg = EmailMessage()
        msg['Subject'] = 'Registration'
        msg['From'] = 'Trend Follower'
        msg['To'] = email
        msg.set_content(message)   



        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.email_name, self.email_password)
            smtp.send_message(msg)
