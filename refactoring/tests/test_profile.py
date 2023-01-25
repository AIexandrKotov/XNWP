from xnwpprofile import XNWPProfile


def test_profile(profile: XNWPProfile) -> None:
    assert profile.saves() == XNWPProfile.loads(profile.saves()).saves()
