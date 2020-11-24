from werkzeug.exceptions import abort


def test_400_bad_request(app, client, captured_templates):
    """
    Create route to abort the request with the 400 Bad Request
    """

    @app.route("/400")
    def bad_request():
        abort(400)

    response = client.get("/400")
    template, context = captured_templates[0]

    assert response.status_code == 400
    assert template.name == "errors/400.html"
    assert "title" in context
    assert context["title"] == "Error 400"


def test_401_unauthorized(app, client, captured_templates):
    """
    Create route to abort the request with the 4001 Unauthorized
    """

    @app.route("/401")
    def unauthorized():
        abort(401)

    response = client.get("/401")
    template, context = captured_templates[0]

    assert response.status_code == 401
    assert template.name == "errors/401.html"
    assert "title" in context
    assert context["title"] == "Error 401"


def test_403_forbidden(app, client, captured_templates):
    """
    Create route to abort the request with the 403 Forbidden
    """

    @app.route("/403")
    def forbidden_error():
        abort(403)

    response = client.get("/403")
    template, context = captured_templates[0]

    assert response.status_code == 403
    assert template.name == "errors/403.html"
    assert "title" in context
    assert context["title"] == "Error 403"


def test_404_not_found(app, client, captured_templates):
    """
    Access a page that does not exist
    """

    response = client.get("/notexistpage")
    template, context = captured_templates[0]

    assert response.status_code == 404
    assert template.name == "errors/404.html"
    assert "title" in context
    assert context["title"] == "Error 404"


def test_405_not_found(app, client, captured_templates):
    """
    Access a page using a method not allowed
    """

    @app.route("/405", methods=["DELETE"])
    def method_not_allowed():
        pass

    response = client.get("/405")
    template, context = captured_templates[0]

    assert response.status_code == 405
    assert template.name == "errors/405.html"
    assert "title" in context
    assert context["title"] == "Error 405"


def test_500_internal_server_error(app, client, captured_templates):
    """
    Create route to abort the request with the 500 Error
    """

    @app.route("/500")
    def internal_server_error():
        abort(500)

    response = client.get("/500")
    template, context = captured_templates[0]

    assert response.status_code == 500
    assert template.name == "errors/500.html"
    assert "title" in context
    assert context["title"] == "Error 500"
