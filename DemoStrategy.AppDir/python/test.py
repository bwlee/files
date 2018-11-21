#encoding: utf-8

from gmsdk import *

import sys
import arrow

class Example(Strategy):
  trade_ready = False
  last_tick = None

  def on_quote_ready(self):
    print("quote ready")
  def on_quote_disconnected(self):
    print("quote disconnected")
 
  def on_trade_ready(self):
    self.trade_ready = True
    print("trade ready")

  def on_trade_disconnected(self):
    print("trade disconnected")
    self.trade_ready = False
 
  def on_tick(self, tick):
    print("tick: ", tick.symbol(), tick.last_price, tick.volume,  tick.last_volume, tick.last_amount, tick.update_time)
    self.last_tick = tick
    if self.trade_ready:
      self.buy_open(tick.symbol(), OrderPriceType.LimitPrice, tick.last_price, 1, 0.0)

  def on_bar(self, bar):
    print("bar: ", bar.symbol(), bar.close, bar.volume, bar.amount, bar.end_time)
 
  def on_exec_rpt(self, rpt):
    print("got rpt", rpt.sec_id)

  def on_order_pendingnew(self, ord):
    print("pendingnew order:", ord.sec_id, ord.volume, ord.price)
  
  def on_order_new(self, ord):
    print("new order:", ord.sec_id, ord.volume, ord.price)

  def on_order_rejected(self, ord):
    print("order rejected:", ord.sec_id, ord.volume, ord.price, ord.reject_reason_detail)
  
  def on_order_partially_filled(self, ord):
    print("order partially filled:", ord.sec_id, ord.volume, ord.price, ord.filled_volume)
  
  def on_order_filled(self, ord):
    print("order filled:", ord.sec_id, ord.volume, ord.price, ord.filled_volume)

  def on_order_cancelled(self, ord):
    print("order cancelled:", ord.sec_id, ord.volume, ord.price)

  def on_cancel_order_rejected(self, ord):
    print("cancel order rejected:", ord.sec_id, ord.volume, ord.price)

  def on_account(self, acc): 
    print("account:", acc.realized_pnl, acc.nav, acc.cum_commission)

  def on_position_open(self, pos): 
    print("pos open:", pos.sec_id, pos.volume, pos.side, pos.price)

  def on_position_close(self, pos): 
    print("pos close:", pos.sec_id, pos.volume, pos.side, pos.price)
  
  def on_timer(self, timer_id):
    print("on timer", timer_id, arrow.now())
    print("positions:", len(self.list_positions(500)))
    tick = self.last_tick
    if tick is None:
      return
    self.buy_open(tick.symbol(), OrderPriceType.LimitPrice, tick.last_price, 1, 0.0)


if __name__ == '__main__':
   s= Example()
   s.local_settle(False)
   s.add_timer(0, s.on_timer, 10*1000*1000) # 1second

   #s.subscribe({'SHFE.ni1901', 'DCE.i1901', 'CFFEX.T1901', 'SHFE.ag1812'}, 5)
   s.subscribe({'CFFEX.TF1901', 'DCE.i1901', 'SHFE.ni1901', 'SHFE.ag1812'})
   #s.subscribe({'CFFEX.XX1901'}, 3)
   s.subscribe({'CFFEX.TF1901', 'DCE.i1901', 'SHFE.ni1901'})
   s.run()
