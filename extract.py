import json
from lxml import html
from utils import read_htmlFile
from db_config import create_table, insert_into_db

TABLE_NAME = 'wendy_information'
base_path = r"C:\Users\hemanshu.marwadi\Desktop\Himanshu Marwadi\x-path\wendy\wendy.html"


def parsel_data(html_data):
    wendy = []
    tree = html.fromstring(html_data)
    wendy_s = {}

    wendy_s['brand_name'] = "Wendy's"
    wendy_s['branch_name'] = tree.xpath('normalize-space(string(//h1[@itemprop="name"]))')

    store_id = tree.xpath('normalize-space(string(//main/@itemid))')
    wendy_s['store_ID'] = store_id.split("#")[-1] if store_id else ""

    wendy_s['cuisine'] = tree.xpath('normalize-space(string(//meta[@itemprop="servesCuisine"]/@content))')
    wendy_s['price'] = tree.xpath('normalize-space(string(//meta[@itemprop="priceRange"]/@content))')
    wendy_s['street_address'] = tree.xpath('normalize-space(string(//span[@class="c-address-street-1"]))')
    wendy_s['city'] = tree.xpath('normalize-space(string(//span[@class="c-address-city"]))')
    wendy_s['state'] = tree.xpath('normalize-space(string(//abbr[@class="c-address-state"]))')
    wendy_s['postalcode'] = tree.xpath('normalize-space(string(//span[@itemprop="postalCode"]))')
    wendy_s['country'] = tree.xpath('normalize-space(string(//abbr[@itemprop="addressCountry"]))')
    wendy_s['latitude'] = tree.xpath('normalize-space(string(//meta[@itemprop="latitude"]/@content))')
    wendy_s['longitude'] = tree.xpath('normalize-space(string(//meta[@itemprop="longitude"]/@content))')
    wendy_s['phone_number'] = tree.xpath('normalize-space(string(//a[@data-ya-track="mainphone"]))')
    wendy_s['restaurant_hours'] = []
    wendy_s['Amenities'] = []
    wendy_s['delivery_partners'] = []
    wendy_s['meta_description'] = tree.xpath('normalize-space(string(//meta[@name="description"]/@content))')
    wendy_s['source_url'] = tree.xpath('normalize-space(string(//link[@rel="canonical"]/@href))')

    timing_hours = tree.xpath('//tr[@itemprop="openingHours"]')
    for hours in timing_hours:
        timing = {}
        timing['day'] = hours.xpath('normalize-space(string(.//td[@class="c-location-hours-details-row-day"]))')
        timing['openingHours'] = hours.xpath('normalize-space(string(.//span[@class="c-location-hours-details-row-intervals-instance-open"]))')
        timing['closingHours'] = hours.xpath('normalize-space(string(.//span[@class="c-location-hours-details-row-intervals-instance-close"]))')
        wendy_s['restaurant_hours'].append(timing)

    amenities = tree.xpath('//span[@itemprop="amenityFeature"]/text()')
    for service in amenities:
        clean_service = " ".join(service.split())
        wendy_s['Amenities'].append(clean_service)

    d_partner = tree.xpath('//a[contains(@class,"LocationInfo-deliveryPartnerLink")]')
    for partner in d_partner:
        link = partner.xpath('normalize-space(.//@href)')
        wendy_s['delivery_partners'].append(link)


    wendy_s['restaurant_hours'] = json.dumps(wendy_s['restaurant_hours'])
    wendy_s['Amenities'] = json.dumps(wendy_s['Amenities'])
    wendy_s['delivery_partners'] = json.dumps(wendy_s['delivery_partners'])

    wendy.append(wendy_s)
    return wendy


def main():
    create_table(table_name=TABLE_NAME)
    raw = read_htmlFile(base_path)
    parsel = parsel_data(raw)

    for result in parsel:
        insert_into_db(table_name=TABLE_NAME, data=result)


if __name__ == "__main__":
    main()