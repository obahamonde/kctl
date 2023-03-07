"""

Test Suites based on Pytest Framework

"""
from names import get_full_name
from kubernetes.services.orm import FQLBaseModel as QM, FQLModel as Q
from kubernetes.utils import uid as get_id, now as get_now , avatar as get_avatar



class Mock(Q):
    """Mock Model for testing purposes"""
    id_:str
    name:str
    picture:str
    created_at:float

def test_type():
    """Test that the type of the class is FQLModelMetaClass"""
    assert type(Q) == type(QM)


def test_schema():
    """Test that the schema of the model is a dictionary"""
    assert type(Mock.__schema__()) == dict

def test_json():
    """Check that the json representation of the model is a string"""
    assert type(Mock.__json__()) == str

def test_create():
    """Test that the create method returns a dictionary
        And that the dictionary contains the id of the record"""
    id_ = get_id()
    now = get_now()
    avatar = get_avatar()
    full_name = get_full_name()
    mock = Mock(id_=id_,name=full_name,picture=avatar,created_at=now).create()
    assert mock['id_'] == id_

def test_save():
    """Test that the save method returns a dictionary
        And that the dictionary contains the id of the record"""
    id_ = get_id()
    now = get_now()
    avatar = get_avatar()
    full_name = get_full_name()
    mock = Mock(id_=id_,name=full_name,picture=avatar,created_at=now).save()
    assert mock['id_'] == id_

def test_find():
    """Test that the find method returns a dictionary
        And that the dictionary contains the id of the record"""
    id_ = get_id()
    now = get_now()
    avatar = get_avatar()
    full_name = get_full_name()
    Mock(id_=id_,name=full_name,picture=avatar,created_at=now).create()
    mock = Mock.find_one("id_",id_)
    assert mock['data']['id_'] == id_

def test_update():
    """Test that the update method returns a dictionary
        And that the dictionary contains the id of the record"""
    id_ = get_id()
    now = get_now()
    avatar = get_avatar()
    full_name = get_full_name()
    Mock(id_=id_,name=full_name,picture=avatar,created_at=now).create()
    mock = Mock.update("id_",id_,{
        "name":"test"
    })
    assert mock['data']['name'] == "test"

def test_delete():
    """Test that the delete method returns a dictionary
        And that the dictionary contains the id of the record"""
    id_ = get_id()
    now = get_now()
    avatar = get_avatar()
    full_name = get_full_name()
    Mock(id_=id_,name=full_name,picture=avatar,created_at=now).create()
    mock = Mock.delete("id_",id_)
    assert mock['data']['id_'] == id_

