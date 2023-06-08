from tests.fixtures import api

import hashlib


TEST_PACKAGE = b"FAKEZIP3904095709145 1904jfas dfj90 329jrffm 23e90 fm2390j"
CHECKSUM = hashlib.md5(TEST_PACKAGE).hexdigest()
FILENAME = "test-package-9.7.4.zip"


def test_installer(api):
    # Delete the package if it exists (cleanup)
    try:
        res = api.delete(f"desktop/installers/{FILENAME}")
    except Exception:
        pass

    # Create installer
    res = api.post(
        "desktop/installers",
        filename=FILENAME,
        version="9.7.4",
        platform="windows",
        pythonVersion="3.7",
        pythonModules={"numpy": "1.2.3"},
    )

    assert res

    res = api.get("desktop/installers")
    assert res

    for installer in res.data.get("installers", []):
        if installer["filename"] != FILENAME:
            continue
        break
    else:
        assert False, "Installer not found"

    assert installer["version"] == "9.7.4"
    assert installer["sources"] == [], "Installer should not have sources at this point"

    # Upload the package

    res = api.raw_put(
        f"desktop/installers/{FILENAME}",
        mime="application/octet-stream",
        data=TEST_PACKAGE,
    )

    assert res
    res = api.get("desktop/installers")
    assert res

    for installer in res.data.get("installers", []):
        if installer["filename"] != FILENAME:
            continue
        break
    else:
        assert False, "Installer not found"

    assert installer["version"] == "9.7.4"
    assert installer["sources"] == [{"type": "server"}]

    # Check the test-package-9

    res = api.raw_get(f"desktop/installers/{FILENAME}")
    assert res == TEST_PACKAGE

    # delete the package

    res = api.delete(f"desktop/installers/{FILENAME}")
    assert res

    # Check the test-package-9

    res = api.raw_get(f"desktop/installers/{FILENAME}")
    assert res != TEST_PACKAGE


def test_dep_packages(api):
    # Delete the package if it exists (cleanup)
    try:
        res = api.delete(f"desktop/dependency_packages/{FILENAME}")
    except Exception:
        pass

    # Create dependency_packages
    res = api.post(
        "desktop/dependency_packages",
        filename=FILENAME,
        platform="windows",
        installerVersion="9.7.4",
        pythonModules={"numpy": "1.2.3"},
    )

    assert res

    res = api.get("desktop/dependency_packages")
    assert res

    for package in res.data.get("packages", []):
        if package["filename"] == FILENAME:
            break
    else:
        assert False, "package not found"

    assert package["installerVersion"] == "9.7.4"
    assert package["platform"] == "windows"
    assert package["sources"] == [], "package should not have sources at this point"

    # Upload the package

    res = api.raw_put(
        f"desktop/dependency_packages/{FILENAME}",
        mime="application/octet-stream",
        data=TEST_PACKAGE,
    )

    assert res
    res = api.get("desktop/dependency_packages")
    assert res

    for package in res.data.get("packages", []):
        if package["filename"] == FILENAME:
            break
    else:
        assert False, "package not found"

    assert package["sources"] == [{"type": "server"}]

    # Check the test-package-9

    res = api.raw_get(f"desktop/dependency_packages/{FILENAME}")
    assert res == TEST_PACKAGE

    # delete the package

    res = api.delete(f"desktop/dependency_packages/{FILENAME}")
    assert res

    # Check the test-package-9

    res = api.raw_get(f"desktop/dependency_packages/{FILENAME}")
    assert res != TEST_PACKAGE
