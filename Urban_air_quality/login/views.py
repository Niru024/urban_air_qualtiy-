from django.shortcuts import render, redirect

from .models import register, login as LoginModel
import logging

logger = logging.getLogger(__name__)

def landing_page(request):
    return render(request, 'login/landingpage.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember_me = request.POST.get('remember_me') == 'on'
        
        if not username or not password:
            return render(request, 'login/login.html', {'error': 'Username and password are required'})
        
        try:
            # Check if user exists in login model
            user_login = LoginModel.objects.get(username=username, password=password)
            
            # Get user details from register model
            user_info = register.objects.get(name=username)
            
            # Store user information in session
            request.session['user_id'] = user_info.id
            request.session['user_name'] = user_info.name
            request.session['user_email'] = user_info.email
            request.session['is_logged_in'] = True
            
            # Handle Remember Me functionality
            if remember_me:
                # Set session to persist for 30 days (2592000 seconds)
                request.session.set_expiry(2592000)
                logger.info(f"User {username} logged in with 'Remember Me' enabled (30 days)")
            else:
                # Session expires when browser closes
                request.session.set_expiry(0)
                logger.info(f"User {username} logged in successfully")
            
            # Redirect to dashboard after successful login
            return redirect('dashboard')
        except LoginModel.DoesNotExist:
            # If login fails, return to login page with error message
            logger.warning(f"Failed login attempt for username: {username}")
            return render(request, 'login/login.html', {'error': 'Invalid username or password'})
        except register.DoesNotExist:
            logger.error(f"User {username} not found in register model")
            return render(request, 'login/login.html', {'error': 'User information not found'})
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return render(request, 'login/login.html', {'error': f'Login failed: {str(e)}'})
    
    return render(request, 'login/login.html')


def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        city = request.POST.get('city', '').strip()
        
        # Validate
        if not name or not email or not password or not city:
            return render(request, 'login/register.html', {'error': 'All fields are required'})
        
        try:
            # Check if email already exists
            if register.objects.filter(email=email).exists():
                logger.warning(f"Registration attempt with existing email: {email}")
                return render(request, 'login/register.html', {'error': 'Email already registered'})
            
            # Create new user in register model
            new_user = register.objects.create(
                name=name,
                email=email,
                password=password,
                city=city
            )
            logger.info(f"New user registered: {name} ({email}) - City: {city} - ID: {new_user.id}")
            
            # Also create login entry
            login_entry = LoginModel.objects.create(
                username=name,
                password=password
            )
            logger.info(f"Login entry created for: {name}")
            
            # Redirect to login page after successful registration with success message
            return render(request, 'login/login.html', {'success': 'Registration successful! Please login with your credentials.'})
        except Exception as e:
            logger.error(f"Registration error for {email}: {str(e)}")
            return render(request, 'login/register.html', {'error': f'Registration failed: {str(e)}'})
    
    return render(request, 'login/register.html')


def logout_view(request):
    # Clear all session data
    logger.info(f"User {request.session.get('user_name')} logged out")
    request.session.flush()
    # Redirect to landing page or login page
    return redirect('login')


def profile_view(request):
    # Check if user is logged in
    if not request.session.get('is_logged_in'):
        return redirect('login')
    
    # Get user information from session
    context = {
        'user_name': request.session.get('user_name', ''),
        'user_email': request.session.get('user_email', ''),
        'user_id': request.session.get('user_id', '')
    }
    return render(request, 'dashboard/profile.html', context)


def aqi_map(request):
    return render(request, 'login/Aqi_map.html')


def help_page(request):
    return render(request, 'login/help.html')

def about_page(request):
    return render(request, 'login/about.html')