from pydantic_remote_config.exceptions import AWSError


def test_aws_error():
    error = AWSError("Failed to do x", RuntimeError("Failed to do x"))
    assert str(error) == "Failed to do x \nRaised Exception: Failed to do x"
