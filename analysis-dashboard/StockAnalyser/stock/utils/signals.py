"""
    Generate Buy/Sell signals from calculated indicators
"""
import pandas as pd
import numpy as np
from collections import Counter


class Signals:
    def __init__(self, ticker, data_df):
        self.ticker = ticker
        self.df = data_df

        # run all member functions starting with 'generate'
        for name in dir(self):
            if name.startswith('generate'):
                method = getattr(self, name)
                method()
        self.overall_signal, self.overall_signal_data = self.computeOverallSignals()

    def generateSMASignals(self):
        """
            sma_x > sma_4x generates a Buy signal otherwise a Sell signal.
        """
        self.df["sma_5_10_signal"] = np.where(self.df["sma_close_5"] > self.df["sma_close_10"], "Buy", "Sell")
        self.df["sma_20_100_signal"] = np.where(self.df["sma_close_20"] > self.df["sma_close_100"], "Buy", "Sell")

    def generateEMASignals(self):
        """
            ema_x > ema_4x generates a Buy signal otherwise a Sell signal.
        """
        self.df["ema_5_10_signal"] = np.where(self.df["ema_close_5"] > self.df["ema_close_10"], "Buy", "Sell")
        self.df["ema_20_100_signal"] = np.where(self.df["ema_close_20"] > self.df["ema_close_100"], "Buy", "Sell")

    def generateMACDSignals(self):
        """
            macd > 0 generates a Buy signal otherwise a Sell signal.
        """
        self.df["macd_signal"] = ["Buy" if x > 0 else "Sell" for x in self.df["macd_close_12_26"]]

    def generateRSISignals(self):
        """
            rsi > 70 indicates stock is Overbought.
            rsi < 30 indicates stock is Oversold.
            rsi otherwise indicates stock is Neutral.
        """
        rsi_signal = []
        for x in self.df["rsi_close_14"]:
            if x>70:
                rsi_signal.append("Overbought")
            elif x<30:
                rsi_signal.append("Oversold")
            else:
                rsi_signal.append("Neutral")
        self.df["rsi_signal"] = rsi_signal

    def generateTRIXSignals(self):
        """
            trix > 0 generates a Buy signal otherwise a Sell signal.
        """
        self.df["trix_signal"] = ["Buy" if x > 0 else "Sell" for x in self.df["trix_close_14"]]

    def generateWRSignals(self):
        """
            wr > -20 indicates stock is Overbought;
            wr < -80 indicates stock is Oversold;
            wr otherwise indicates stock is Neutral;
        """
        wr_signal = []
        for x in self.df["wr_close_14"]:
            if x>-20:
                wr_signal.append("Overbought")
            elif x<-80:
                wr_signal.append("Oversold")
            else:
                wr_signal.append("Neutral")
        self.df["wr_signal"] = wr_signal

    def generateCCISignals(self):
        """
            cci > 100 generates a Buy signal;
            cci < -100 generates a Sell signal;
            cci otherwise indicates stock is Neutral;
        """
        cci_signal = []
        for x in self.df["cci_tp_20"]:
            if x > 100:
                cci_signal.append("Buy")
            elif x<-100:
                cci_signal.append("Sell")
            else:
                cci_signal.append("Neutral")
        self.df["cci_signal"] = cci_signal

    def generateATRSignals(self):
        """
            weighted_atr is the normalized valued of ATR, obtained by dividing it by the Close price. Over here 5 day EMA is used.
            weighted_atr value above 0.05 shows High Volatility otherwise Low Volatility
        """
        weighted_atr = self.df["atr_close_14"]/self.df["ema_close_5"]
        self.df["atr_signal"] = ["High Volatility" if x>0.05 else "Low Volatility" for x in weighted_atr]

    def generateMFISignals(self):
        """
            mfi > 80 indicates stock is Overbought;
            mfi < 20 indicates stock is Oversold;
            mfi otherwise indicates stock is Neutral;
        """
        mfi_signal = []
        for x in self.df["mfi_tp|volume_15"]:
            if x < 20:
                mfi_signal.append("Oversold")
            elif x > 80:
                mfi_signal.append("Overbought")
            else:
                mfi_signal.append("Neutral")
        self.df["mfi_signal"] = mfi_signal


    def generateCMFSignals(self):
        """
            cmf > 0 generates a Buy signal otherwise a Sell signal.
        """
        self.df["cmf_21_signal"] = ["Buy" if x > 0 else "Sell" for x in self.df["cmf_close|volume_21"]]

    def generateSTOCHRSISignals(self):
        """
            stochrsi > 50 generates a Buy signal otherwise a Sell signal.
        """
        self.df["stochrsi_signal"] = ["Buy" if x > 50 else "Sell" for x in self.df["stochrsi_rsi_14"]]

    def generateOBVSignals(self):
        """
            when obv and price increase together a Buy signal is generated.
            when obv and price decrease together a Sell signal is generated.
        """
        obv_signal = []
        obv_changes = self.df["obv_close|volume_1"] - self.df["obv_close|volume_1"].shift()
        ema_5_changes = self.df["ema_close_5"] - self.df["ema_close_5"].shift()
        for x,y in zip(obv_changes, ema_5_changes):
            if x>0 and y>0:
                obv_signal.append("Buy")
            elif x<0 and y<0:
                obv_signal.append("Sell")
            elif x == 0 and y == 0:
                obv_signal.append("Neutral")
            else:
                obv_signal.append("Divergence")
        self.df["obv_1_signal"] = obv_signal

    def generateSTOCHSignals(self):
        """
            stoch generates a Buy signal when it crosses 20 from below;
            stoch generates a Sell signal when it crosses 80 from above;
            stoch otherwise indicates stock is Neutral.
        """
        stoch_signal = []
        for cur,prev in zip(self.df["stoch_14"], self.df["stoch_14"].shift()):
            if cur >= 20 and prev < 20:
                stoch_signal.append("Buy")
            elif cur < 80 and prev >= 80:
                stoch_signal.append("Sell")
            else:
                stoch_signal.append("Neutral")
        self.df["stoch_signal"] = stoch_signal

    def generatePGOSignals(self):
        """
            pgo > 3 gives Long indication;
            pgo < -3  gives Short indication;
            pgo otherwise stays Neutral;
        """
        pgo_signal = []
        for x in self.df["pgo_close_14"]:
            if x > 3:
                pgo_signal.append("Long")
            elif x < -3:
                pgo_signal.append("Short")
            else:
                pgo_signal.append("Neutral")
        self.df["pgo_signal"] = pgo_signal

    def computeOverallSignals(self, reference_period=5):
        all_cols = list(self.df.columns.values)
        overall = []
        overall_data = {}
        signal_columns = list(filter(lambda x: x.find("_signal") != -1, all_cols))
        for col in signal_columns:
            signal_data = self.df[col]
            last_period = Counter(list(signal_data[-reference_period:].values)).most_common(1)[0]
            overall_data[col] = {
                "signal": last_period[0],
                "freq": last_period[1],
                "reference": reference_period
            }
            overall += list(signal_data[-reference_period:].values)
        overall = Counter(list(filter(lambda x: x in ["Buy", "Sell"], overall))).most_common(1)[0][0]
        return overall, overall_data

    def getDF(self):
        return self.df
