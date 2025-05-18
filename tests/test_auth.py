import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user_data():
  """Fixture para datos de usuario de prueba."""
  return {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'securepassword123',
    'first_name': 'Test',
    'last_name': 'User',
    'identification': '12345678-9',
    'position': 'Fiscal',
    'department': 'Fiscalía Central',
    'phone': '+56912345678',
  }

@pytest.fixture
def user(db, user_data):
  """Fixture para crear un usuario en la base de datos."""
  user = User.objects.create_user(
    username=user_data['username'],
    email=user_data['email'],
    password=user_data['password'],
    first_name=user_data['first_name'],
    last_name=user_data['last_name']
  )
  user.identification = user_data['identification']
  user.position = user_data['position']
  user.department = user_data['department']
  user.phone = user_data['phone']
  user.save()
  return user

@pytest.mark.django_db
def test_user_create(user_data):
  """Test para verificar la creación de un usuario."""
  # Crear un usuario usando los datos de prueba
  user = User.objects.create_user(
    username=user_data['username'],
    email=user_data['email'],
    password=user_data['password']
  )
  
  # Verificar que el usuario se creó correctamente
  assert user.username == user_data['username']
  assert user.email == user_data['email']
  assert user.check_password(user_data['password'])

@pytest.mark.django_db
def test_user_login(client, user, user_data):
  """Test para verificar el login de un usuario."""
  # Obtener URL de login
  login_url = reverse('authentication:login')
  
  # Intentar login con credenciales incorrectas
  response = client.post(login_url, {
    'username': user_data['username'],
    'password': 'wrong-password'
  })
  
  # Verificar que el login falló
  assert response.status_code == 200  # Se queda en la página de login
  
  # Intentar login con credenciales correctas
  response = client.post(login_url, {
    'username': user_data['username'],
    'password': user_data['password']
  }, follow=True)
  
  # Verificar que el login fue exitoso
  assert response.status_code == 200
  assert response.wsgi_request.user.is_authenticated

@pytest.mark.django_db
def test_user_logout(client, user, user_data):
  """Test para verificar el logout de un usuario."""
  # Login
  client.login(username=user_data['username'], password=user_data['password'])
  
  # Verificar que el usuario está autenticado
  assert client.session['_auth_user_id'] == str(user.id)
  
  # Obtener URL de logout
  logout_url = reverse('authentication:logout')
  
  # Hacer logout
  response = client.get(logout_url, follow=True)
  
  # Verificar que el logout fue exitoso
  assert response.status_code == 200
  assert not response.context['user'].is_authenticated 