import random

import pytest

from src.helpers.schema_validator import is_schema_right


class TestGetListOfPetsByStatus:
    """
    This class checks whether the GET - /findByStatus API works as expected.
    """

    @pytest.mark.positive
    @pytest.mark.test
    @pytest.mark.parametrize("pet_status", ["available", "pending", "sold"])
    def test_get_list_of_pets_by_status(self, session, pet_status):
        """
        Sends a GET request to get list of pets by status.
        Test checks the following
            - Response code is 200
            - Response schema
        """
        resp = session.get("/findByStatus", params={"status": pet_status})

        assert (
            resp.status_code == 200
        ), f"Response code mismatch. Expected: 200 - Got: {resp.status_code}"

        is_resp_valid, exc = is_schema_right(
            resp.json(), "src/schemas/responses/get_list_of_pets.json"
        )

        try:
            assert is_resp_valid
        except AssertionError:
            raise exc

    @pytest.mark.negative
    def test_invalid_pet_status(self, session):
        """
        Sends a GET request with invalid status.
        Test checks the following,
            - Response code is 200
            - Response should be empty
        """
        resp = session.get("findByStatus", params={"status": "invalid_status"})

        assert (
            resp.status_code == 200
        ), f"Response code mismatch. Expected: 200 - Got: {resp.status_code}"

        assert (
            length_of_response := len(resp.json()) == 0
        ), f"The response length is 0, but returned response has '{length_of_response}' length"


class TestCreateNewPet:
    """
    This class examines the API for creation of new pets works as expected.
    """

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "pet_status,category,tags,name",
        [
            ("available", "dakhund", ("tag1", "tag2"), "joshmax"),
            ("pending", "retriever", ("tag3", "tag4"), "luna"),
            ("sold", "maltese", ("tag5", "tag6", "tag7"), "bella"),
        ],
    )
    def test_create_new_pet(self, session, pet_status, category, tags, name):
        """
        Sends a POST request to create a new pet.
        It checks the following,
            - Response is 200
            - Whether the response has correct schema
        """

        body = {
            "id": 0,
            "category": {"id": 0, "name": category},
            "name": name,
            "tags": [{"id": ind, "name": tag} for ind, tag in enumerate(tags)],
            "status": pet_status,
        }
        resp = session.post("", json=body)

        assert (
            resp.status_code == 200
        ), f"Response code mismatch. Expected: 200 - Got: {resp.status_code}"

        assert resp.json()["tags"] == [
            {"id": ind, "name": tag} for ind, tag in enumerate(tags)
        ]
        assert resp.json()["category"]["name"] == category
        assert resp.json()["status"] == pet_status

        is_resp_valid, exc = is_schema_right(
            resp.json(), "src/schemas/responses/newly_created_pet.json"
        )

        try:
            assert is_resp_valid
        except AssertionError:
            raise exc

    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="I think it should return 400, but it returns 500"
    )  # expected fail
    @pytest.mark.parametrize("invalid_input", [{}, "invalid", 23, False])
    def test_try_to_create_with_invalid_body(self, session, invalid_input):
        """
        Sends a POST request to create new pets.
        It checks the following,
            - Response is 400
        """
        resp = session.post("", json=invalid_input)  # accepts only an object/json

        assert (
            resp.status_code == 400
        ), f"Response code mismatch. Expected: 400 - Got: {resp.status_code}"


class TestUpdateExistingPet:
    """
    This class checks whether updating/changing an existing data works as expected.
    """

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session):
        resp = session.get(
            "findByStatus",
            params={"status": random.choice(["available", "pending", "sold"])},
        )
        resp_json = resp.json()

        self.random_pet_json = random.choice(resp_json)

    @pytest.mark.positive
    @pytest.mark.parametrize(
        "tag_name, new_value",
        [
            ("category", {"id": 0, "name": "new_category"}),
            ("tags", [{"id": 0, "name": "new_tag_1"}, {"id": 1, "name": "new_tag_2"}]),
            ("status", random.choice(["sold", "available", "pending"])),
        ],
    )
    def test_update_a_given_pet_with_body(self, session, tag_name, new_value):
        """
        Sends a PUT request to update an existing pet.
        It checks the following,
            - Response is 200
            - Whether the response has the correct schema
        """
        body = {**self.random_pet_json, tag_name: new_value}
        resp = session.put("", json=body)

        assert (
            resp.status_code == 200
        ), f"Response code mismatch. Expected: 200 - Got: {resp.status_code}"

        assert (
            resp.json()[tag_name] == new_value
        ), f"The '{tag_name}' is not equal to '{new_value}', but {resp.json()[tag_name]}"

        is_resp_valid, exc = is_schema_right(
            resp.json(), "src/schemas/responses/newly_created_pet.json"
        )

        try:
            assert is_resp_valid
        except AssertionError:
            raise exc

    @pytest.mark.positive
    @pytest.mark.parametrize("new_name", ["new_name_11", "new_name_22"])
    def test_update_a_given_pet_by_id(self, session, new_name):
        """
        Sends a POST request to update an existing pet by given id.
        It checks the following,
            - Response is 200
        """
        pet_id = self.random_pet_json["id"]

        new_status = random.choice(
            [
                st
                for st in ["sold", "available", "pending"]
                if st == self.random_pet_json["status"]
            ]
        )

        resp = session.post(
            f"/{pet_id}", params={"name": new_name, "status": new_status}
        )

        assert (
            resp.status_code == 200
        ), f"Response code mismatch. Expected: 200 - Got: {resp.status_code}"

    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="I think it should return 400, but it return 500"
    )  # expected fail
    @pytest.mark.parametrize("invalid_input", ["invalid", 23, False])
    def test_try_to_update_with_invalid_body(self, session, invalid_input):
        """
        Sends a PUT request to show that it is not possible to update a pat with invalid input.
        It checks the following,
            - Response is 400
        """
        resp = session.put("", json=invalid_input)

        assert (
            resp.status_code == 400
        ), f"Response code mismatch. Expected: 400 - Got: {resp.status_code}"

    @pytest.mark.negative
    @pytest.mark.xfail(
        reason="I think it should return 404, but it return 500"
    )  # expected fail
    def test_try_to_create_with_invalid_id(self, session):
        """
        Sends a PUT request to with invalid id to ensure that
            it is not possible to update something with
                invalid/not-existing id.
        It checks the following,
            - Response is 404 (because such object couldn't be found with given id)
        """
        body = {**self.random_pet_json, "id": "invalid_id"}
        resp = session.put("", json=body)

        assert (
            resp.status_code == 404
        ), f"Response code mismatch. Expected: 404 - Got: {resp.status_code}"


class TestDeleteExistingPet:
    """
    This class tests the deleting request.
    """

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, session):
        resp = session.get(
            "findByStatus",
            params={"status": random.choice(["available", "pending", "sold"])},
        )
        resp_json = resp.json()

        self.random_pet_json = random.choice(resp_json)

    @pytest.mark.positive
    def test_delete_existing_pet(self, session):
        """
        Sends a DELETE request to delete an existing pet.
        It checks the following,
            - Response is either 200 or 204
            - Checks if object is deleted
        """
        pet_id = self.random_pet_json["id"]

        resp = session.delete(f"/{pet_id}")
        assert resp.status_code in (
            200,
            204,
        ), f"Response code\n\tExpected: (200|204)\n\tGot: {resp.status_code}"

        resp = session.get(f"/{pet_id}")
        assert (
            resp.status_code == 404
        ), f"Response code mismatch. Expected: 404 - Got: {resp.status_code}"

    @pytest.mark.negative
    def test_try_to_delete_unexisting_id(self, session):
        """
        Sends a DELETE request with an unexisting id.
        It checks the following,
            - Response is 404
        """
        pet_id = "unexisting_id"

        resp = session.delete(f"/{pet_id}")
        assert (
            resp.status_code == 404
        ), f"Response code mismatch. Expected: 404 - Got: {resp.status_code}"
