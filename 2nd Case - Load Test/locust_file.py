import random
from locust import HttpUser, task, between, User, run_single_user
from lxml import html
from urllib.parse import urlencode


class ProductQueryLoadTestUser(HttpUser):
    wait_time = between(3, 5)

    def on_start(self):
        """
        Set several examples for querying.
        """
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
                "Accept-Language": "tr-TR,tr;q=0.9",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )
        self.special_charachters = ["ä", "½", "%", ":", ".", "Â"]
        self.search_queries = [
            "kitap",
            "bilgisayar",
            "telefon",
            "gömlek",
            "erkek ayakkabı",
            "kitap okuyucu",
        ]
        self.query_by_page_number = {"q": "telefon", "pg": random.randint(2, 5)}
        self.query_by_filter = {"q": "nevresim", "olculer": "200 x 220"}
        self.query_sorting = [
            {"srt": "SALES_VOLUME", "q": "pilates"},
            {"srt": "PRICE_HIGH", "q": "pilates"},
            {"srt": "NEWEST", "q": "pilates"},
        ]

    @task(3)
    def basic_query(self):
        search_query = random.choice(self.search_queries)

        with self.client.get(f"/arama?q={search_query}", catch_response=True) as resp:
            if st_code := resp.status_code != 200:
                resp.failure(
                    f"Basic Query Failed - Server response - Expected: 200 - Returned {st_code}."
                )

            tree = html.fromstring(resp.content)
            products = tree.xpath("//a[@class='product-item']")

            if not products:
                resp.failure(
                    f"Basic Query Failed - No products are available for query '{search_query}'"
                )

    @task(1)
    def empty_query(self):
        with self.client.get(f"/arama?q=", catch_response=True) as resp:
            if st_code := resp.status_code != 302:
                resp.failure(
                    f"Empty Query Failed - Server response - Expected: 302 - Returned {st_code}."
                )

            if location_header := resp.headers.get("Location") != "\\":
                resp.failure(
                    f"Empty Query Failed - 'Location' in headers is {location_header} instead of ''."
                )

    @task(1)
    def not_existing_product_query(self):
        with self.client.get(
            "/arama?q=NOT_EXISTING_PRODUCT", catch_response=True
        ) as resp:
            if st_code := resp.status_code != 200:
                resp.failure(
                    f"Not Existing Product Query Failed - Server response - Expected: 200 - Returned {st_code}."
                )
            if "Aradığını bulamadık.".encode() not in resp.content:
                resp.failure(
                    f"Not Existing Product Query Failed - Content doesn't include no product could be found message"
                )
            if "Aşağıdaki önerileri deneyebilirsin.".encode() not in resp.content:
                resp.failure(
                    f"Not Existing Product Query Failed - Content doesn't include suggestions"
                )

    @task(1)
    def query_specials_charachters(self):
        random.choice(self.special_charachters)

        with self.client.get("/arama?q=ä", catch_response=True) as resp:
            if st_code := resp.status_code != 302:
                resp.failure(
                    f"Query with Special Characters Failed - Server response - Expected: 302 - Returned {st_code}."
                )

            if location_header := resp.headers.get("Location") != "\\":
                resp.failure(
                    f"Query with Special Characters Failed - 'Location' in headers is {location_header} instead of ''."
                )

    @task(2)
    def query_by_page_number(self):
        with self.client.get(
            f"/arama", params=self.query_by_page_number, catch_response=True
        ) as resp:
            if st_code := resp.status_code != 200:
                resp.failure(
                    f"Query by Page Number Failed - Server response - Expected: 200 - Returned {st_code}."
                )

            tree = html.fromstring(resp.content)
            products = tree.xpath("//a[@class='product-item']")

            if not products:
                resp.failure(
                    f"Query by Page Number Failed - No products are available for query '{urlencode(self.query_by_page_number)}'"
                )

    @task(2)
    def query_by_filter(self):
        with self.client.get(
            f"/arama", params=self.query_by_filter, catch_response=True
        ) as resp:
            if st_code := resp.status_code != 200:
                resp.failure(
                    f"Query by Filter Failed - Server response - Expected: 200 - Returned {st_code}."
                )

            tree = html.fromstring(resp.content)
            products = tree.xpath("//a[@class='product-item']")

            if not products:
                resp.failure(
                    f"Query by Filter Failed - No products are available for query '{urlencode(self.query_by_filter)}'"
                )

    @task(2)
    def query_sorting(self):
        random_query_sort = random.choice(self.query_sorting)

        with self.client.get(
            f"/arama", params=random_query_sort, catch_response=True
        ) as resp:
            if st_code := resp.status_code != 200:
                resp.failure(
                    f"Query Sorting Failed - Server response - Expected: 200 - Returned {st_code}."
                )

            tree = html.fromstring(resp.content)
            products = tree.xpath("//a[@class='product-item']")

            if not products:
                resp.failure(
                    f"Query Sorting Failed - No products are available for query '{urlencode(random_query_sort)}'"
                )
