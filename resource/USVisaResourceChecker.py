from dataclasses import dataclass, field
from playwright.sync_api import sync_playwright, Playwright, expect
import time
from . import ResourceChecker
from .request import DateRangeRequest
from .response import Response
from messaging import Message
from util.decorators import non_null_args
from typing import List
import datetime as dt
import json

JS_SCRIPT = ("() => {"
			"var req = new XMLHttpRequest();"
             f"req.open('GET', '%s', false);"
             "req.setRequestHeader('Accept', 'application/json, text/javascript, */*; q=0.01');"
             "req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');"
             "req.send(null);"
             "return req.responseText;"
             "};")
DATE_FORMAT = "%Y-%m-%d"
@dataclass
class USVisaResponse(Response):
	available_dates: List[str] = field(default_factory=lambda: [])
	name_override: str = None

	def to_message(self) -> Message:
		if self.error:
			return Message(is_error=True, body=self.error.__str__())

		if not self.available_dates:
			return Message()

		values = self.name_override if self.name_override else self.available_dates

		message_body = (
			f'Found dates for US Visa: {[d.strftime(DATE_FORMAT) for d in self.available_dates]}')

		return Message(body=message_body)

class USVisaResourceChecker(ResourceChecker):
	# https://ais.usvisa-info.com/en-ug/niv/schedule/50295138/appointment

	@non_null_args
	def __init__(self, embassy_id, schedule_id, facility_id, user_email, password): 
		self.dates_url = f"https://ais.usvisa-info.com/{embassy_id}/niv/schedule/{schedule_id}/appointment/days/{facility_id}.json?appointments[expedite]=false"
		self.sign_in_url = f"https://ais.usvisa-info.com/{embassy_id}/niv/users/sign_in"
		self.user_email = user_email
		self.password = password

	def check_resource(self, date_range: DateRangeRequest):

		available_dates = []

		def run(playwright: Playwright):
		    chromium = playwright.chromium
		    browser = chromium.launch()
		    page = browser.new_page()
		    page.goto(self.sign_in_url)
		    page.get_by_label("Email").fill(self.user_email)
		    page.get_by_label("Password").fill(self.password)
		    page.locator(".icheckbox").click()
		    page.get_by_role("button", name="Sign in").click()
		    expect(page.get_by_text("Continue")).to_be_visible()
		    resp = page.evaluate(JS_SCRIPT % self.dates_url)
		    resp = json.loads(resp)
		    for d in resp:
		    	date = d["date"]
		    	date = dt.datetime.strptime(date, DATE_FORMAT)
		    	if date >= date_range.start_date and date <= date_range.end_date:
		    		available_dates.append(date)

		    browser.close()

		with sync_playwright() as playwright:
			try:
		    	run(playwright)
		    except:
		    	return USVisaResponse(available_dates=available_dates, is_error=True)

		return USVisaResponse(available_dates=available_dates)

