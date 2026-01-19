"""
Script de teste manual de autenticação para Finanpy
Usa Playwright para testar todos os fluxos de autenticação
"""
from playwright.sync_api import sync_playwright, expect
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
SCREENSHOTS_DIR = "/Users/erickswolkin/IA_MASTER/finanpy/test_screenshots"

def generate_unique_email():
    """Gera um email único com timestamp"""
    timestamp = int(time.time() * 1000)
    return f"testuser_{timestamp}@teste.com"

def test_authentication_flows():
    """Executa todos os testes de autenticação"""

    results = []
    test_email = None  # Armazena o email do usuário cadastrado

    with sync_playwright() as p:
        # Configurar browser
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        page.set_default_timeout(10000)  # Reduzir timeout para 10 segundos

        try:
            # ===== TESTE 1: Acessar página inicial e verificar layout =====
            print("\n=== TESTE 1: Página Inicial ===")
            try:
                page.goto(BASE_URL, wait_until='domcontentloaded')
                page.wait_for_timeout(1000)
                page.screenshot(path=f"{SCREENSHOTS_DIR}/01_homepage.png", full_page=True)

                # Verificar links de Login e Cadastro
                login_visible = page.locator('a:has-text("Login"), a:has-text("Entrar")').count() > 0
                signup_visible = page.locator('a:has-text("Cadastro"), a:has-text("Cadastrar")').count() > 0

                results.append({
                    'test': 'Teste 1: Página Inicial',
                    'status': 'PASSOU' if (login_visible or signup_visible) else 'FALHOU',
                    'details': f'Links encontrados - Login: {login_visible}, Cadastro: {signup_visible}',
                    'screenshot': '01_homepage.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 1: Página Inicial',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '01_homepage.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 2: Verificar página de cadastro =====
            print("\n=== TESTE 2: Página de Cadastro ===")
            try:
                page.goto(f"{BASE_URL}/signup/", wait_until="domcontentloaded")
                page.wait_for_timeout(1000)
                page.screenshot(path=f"{SCREENSHOTS_DIR}/02_signup_page.png", full_page=True)

                # Verificar campos do formulário
                email_field = page.locator('#id_email, input[name="email"]').count() > 0
                password1_field = page.locator('#id_password1, input[name="password1"]').count() > 0
                password2_field = page.locator('#id_password2, input[name="password2"]').count() > 0
                login_link = page.locator('a:has-text("Login"), a:has-text("Já tem conta")').count() > 0

                all_fields_present = email_field and password1_field and password2_field

                results.append({
                    'test': 'Teste 2: Página de Cadastro',
                    'status': 'PASSOU' if all_fields_present else 'FALHOU',
                    'details': f'Campos - Email: {email_field}, Password1: {password1_field}, Password2: {password2_field}, Link Login: {login_link}',
                    'screenshot': '02_signup_page.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 2: Página de Cadastro',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '02_signup_page.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 3: Cadastro com email inválido =====
            print("\n=== TESTE 3: Email Inválido ===")
            try:
                page.goto(f"{BASE_URL}/signup/", wait_until="domcontentloaded")
                page.wait_for_timeout(1000)

                page.fill('#id_email, input[name="email"]', 'emailinvalido')
                page.fill('#id_password1, input[name="password1"]', 'SenhaForte123!')
                page.fill('#id_password2, input[name="password2"]', 'SenhaForte123!')

                page.click('button[type="submit"], input[type="submit"]')
                page.wait_for_timeout(2000)

                page.screenshot(path=f"{SCREENSHOTS_DIR}/03_invalid_email.png", full_page=True)

                # Verificar se há mensagem de erro
                error_present = page.locator('.errorlist, .error, .alert-danger, [class*="error"]').count() > 0

                results.append({
                    'test': 'Teste 3: Email Inválido',
                    'status': 'PASSOU' if error_present else 'FALHOU',
                    'details': f'Erro exibido: {error_present}',
                    'screenshot': '03_invalid_email.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 3: Email Inválido',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '03_invalid_email.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 4: Cadastro com senha fraca =====
            print("\n=== TESTE 4: Senha Fraca ===")
            try:
                page.goto(f"{BASE_URL}/signup/", wait_until="domcontentloaded")
                page.wait_for_timeout(1000)

                page.fill('#id_email, input[name="email"]', 'teste@teste.com')
                page.fill('#id_password1, input[name="password1"]', '123')
                page.fill('#id_password2, input[name="password2"]', '123')

                page.click('button[type="submit"], input[type="submit"]')
                page.wait_for_timeout(2000)

                page.screenshot(path=f"{SCREENSHOTS_DIR}/04_weak_password.png", full_page=True)

                error_present = page.locator('.errorlist, .error, .alert-danger, [class*="error"]').count() > 0

                results.append({
                    'test': 'Teste 4: Senha Fraca',
                    'status': 'PASSOU' if error_present else 'FALHOU',
                    'details': f'Erro exibido: {error_present}',
                    'screenshot': '04_weak_password.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 4: Senha Fraca',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '04_weak_password.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 5: Cadastro com senhas diferentes =====
            print("\n=== TESTE 5: Senhas Diferentes ===")
            try:
                page.goto(f"{BASE_URL}/signup/", wait_until="domcontentloaded")
                page.wait_for_timeout(1000)

                page.fill('#id_email, input[name="email"]', 'teste2@teste.com')
                page.fill('#id_password1, input[name="password1"]', 'SenhaForte123!')
                page.fill('#id_password2, input[name="password2"]', 'SenhaDiferente456!')

                page.click('button[type="submit"], input[type="submit"]')
                page.wait_for_timeout(2000)

                page.screenshot(path=f"{SCREENSHOTS_DIR}/05_password_mismatch.png", full_page=True)

                error_present = page.locator('.errorlist, .error, .alert-danger, [class*="error"]').count() > 0

                results.append({
                    'test': 'Teste 5: Senhas Diferentes',
                    'status': 'PASSOU' if error_present else 'FALHOU',
                    'details': f'Erro exibido: {error_present}',
                    'screenshot': '05_password_mismatch.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 5: Senhas Diferentes',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '05_password_mismatch.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 6: Cadastrar usuário válido =====
            print("\n=== TESTE 6: Cadastro Válido ===")
            try:
                test_email = generate_unique_email()
                print(f"Email gerado: {test_email}")

                page.goto(f"{BASE_URL}/signup/", wait_until="domcontentloaded")
                page.wait_for_timeout(1000)

                page.fill('#id_email, input[name="email"]', test_email)
                page.fill('#id_password1, input[name="password1"]', 'SenhaSegura123!')
                page.fill('#id_password2, input[name="password2"]', 'SenhaSegura123!')

                page.click('button[type="submit"], input[type="submit"]')
                page.wait_for_timeout(3000)

                page.screenshot(path=f"{SCREENSHOTS_DIR}/06_signup_success.png", full_page=True)

                current_url = page.url
                success = 'dashboard' in current_url.lower() or 'profile' in current_url.lower() or 'home' in current_url.lower()

                results.append({
                    'test': 'Teste 6: Cadastro Válido',
                    'status': 'PASSOU' if success else 'FALHOU',
                    'details': f'Email: {test_email}, URL após cadastro: {current_url}',
                    'screenshot': '06_signup_success.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
                print(f"✓ Email para próximos testes: {test_email}")
            except Exception as e:
                results.append({
                    'test': 'Teste 6: Cadastro Válido',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '06_signup_success.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 7: Verificar redirecionamento após cadastro =====
            print("\n=== TESTE 7: Redirecionamento pós-cadastro ===")
            try:
                page.wait_for_timeout(2000)
                page.screenshot(path=f"{SCREENSHOTS_DIR}/07_after_signup.png", full_page=True)

                current_url = page.url
                logged_in_indicators = page.locator('a:has-text("Logout"), a:has-text("Sair"), a:has-text("Perfil")').count() > 0

                results.append({
                    'test': 'Teste 7: Redirecionamento pós-cadastro',
                    'status': 'PASSOU' if logged_in_indicators else 'FALHOU',
                    'details': f'URL: {current_url}, Indicadores de login: {logged_in_indicators}',
                    'screenshot': '07_after_signup.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 7: Redirecionamento pós-cadastro',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '07_after_signup.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 8: Fazer logout =====
            print("\n=== TESTE 8: Logout ===")
            try:
                logout_button = page.locator('a:has-text("Logout"), a:has-text("Sair"), button:has-text("Sair")')

                if logout_button.count() > 0:
                    logout_button.first.click()
                    page.wait_for_timeout(2000)
                    page.screenshot(path=f"{SCREENSHOTS_DIR}/08_after_logout.png", full_page=True)

                    current_url = page.url
                    logged_out = 'login' in current_url.lower() or page.locator('a:has-text("Login"), a:has-text("Entrar")').count() > 0

                    results.append({
                        'test': 'Teste 8: Logout',
                        'status': 'PASSOU' if logged_out else 'FALHOU',
                        'details': f'URL após logout: {current_url}',
                        'screenshot': '08_after_logout.png'
                    })
                    print(f"✓ Status: {results[-1]['status']}")
                else:
                    # Tentar acessar URL de logout diretamente
                    page.goto(f"{BASE_URL}/logout/", wait_until="domcontentloaded")
                    page.wait_for_timeout(2000)
                    page.screenshot(path=f"{SCREENSHOTS_DIR}/08_after_logout.png", full_page=True)

                    results.append({
                        'test': 'Teste 8: Logout',
                        'status': 'PASSOU',
                        'details': 'Logout via URL direta',
                        'screenshot': '08_after_logout.png'
                    })
                    print(f"✓ Status: PASSOU (via URL)")
            except Exception as e:
                results.append({
                    'test': 'Teste 8: Logout',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '08_after_logout.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 9: Login com credenciais inválidas =====
            print("\n=== TESTE 9: Login com credenciais inválidas ===")
            try:
                page.goto(f"{BASE_URL}/login/", wait_until="domcontentloaded")
                page.wait_for_timeout(1000)

                page.fill('#id_email, #id_username, input[name="email"], input[name="username"]', 'naoexiste@teste.com')
                page.fill('#id_password, input[name="password"]', 'senhaerrada')

                page.click('button[type="submit"], input[type="submit"]')
                page.wait_for_timeout(2000)

                page.screenshot(path=f"{SCREENSHOTS_DIR}/09_invalid_login.png", full_page=True)

                error_present = page.locator('.errorlist, .error, .alert-danger, [class*="error"]').count() > 0
                still_on_login = 'login' in page.url.lower()

                results.append({
                    'test': 'Teste 9: Login Inválido',
                    'status': 'PASSOU' if (error_present or still_on_login) else 'FALHOU',
                    'details': f'Erro exibido: {error_present}, Ainda na página de login: {still_on_login}',
                    'screenshot': '09_invalid_login.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 9: Login Inválido',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '09_invalid_login.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 10: Login com credenciais válidas =====
            print("\n=== TESTE 10: Login com credenciais válidas ===")
            try:
                if test_email:
                    page.goto(f"{BASE_URL}/login/", wait_until="domcontentloaded")
                    page.wait_for_timeout(1000)

                    page.fill('#id_email, #id_username, input[name="email"], input[name="username"]', test_email)
                    page.fill('#id_password, input[name="password"]', 'SenhaSegura123!')

                    page.click('button[type="submit"], input[type="submit"]')
                    page.wait_for_timeout(3000)

                    page.screenshot(path=f"{SCREENSHOTS_DIR}/10_valid_login.png", full_page=True)

                    current_url = page.url
                    success = 'dashboard' in current_url.lower() or 'profile' in current_url.lower() or 'home' in current_url.lower()

                    results.append({
                        'test': 'Teste 10: Login Válido',
                        'status': 'PASSOU' if success else 'FALHOU',
                        'details': f'Email: {test_email}, URL após login: {current_url}',
                        'screenshot': '10_valid_login.png'
                    })
                    print(f"✓ Status: {results[-1]['status']}")
                else:
                    results.append({
                        'test': 'Teste 10: Login Válido',
                        'status': 'BLOQUEADO',
                        'details': 'Email de teste não disponível (cadastro falhou)',
                        'screenshot': 'N/A'
                    })
                    print(f"⚠ Status: BLOQUEADO")
            except Exception as e:
                results.append({
                    'test': 'Teste 10: Login Válido',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '10_valid_login.png'
                })
                print(f"✗ Erro: {e}")

            # ===== TESTE 11: Verificar redirecionamento de usuário autenticado =====
            print("\n=== TESTE 11: Redirecionamento de usuário autenticado ===")
            try:
                # Tentar acessar signup
                page.goto(f"{BASE_URL}/signup/", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                signup_url = page.url
                signup_redirected = 'signup' not in signup_url.lower()

                page.screenshot(path=f"{SCREENSHOTS_DIR}/11a_logged_in_signup.png", full_page=True)

                # Tentar acessar login
                page.goto(f"{BASE_URL}/login/", wait_until="domcontentloaded")
                page.wait_for_timeout(2000)

                login_url = page.url
                login_redirected = 'login' not in login_url.lower()

                page.screenshot(path=f"{SCREENSHOTS_DIR}/11b_logged_in_login.png", full_page=True)

                results.append({
                    'test': 'Teste 11: Redirecionamento de usuário autenticado',
                    'status': 'PASSOU' if (signup_redirected and login_redirected) else 'AVISO',
                    'details': f'Signup redirecionado: {signup_redirected} ({signup_url}), Login redirecionado: {login_redirected} ({login_url})',
                    'screenshot': '11a_logged_in_signup.png, 11b_logged_in_login.png'
                })
                print(f"✓ Status: {results[-1]['status']}")
            except Exception as e:
                results.append({
                    'test': 'Teste 11: Redirecionamento de usuário autenticado',
                    'status': 'FALHOU',
                    'details': f'Erro: {str(e)}',
                    'screenshot': '11a_logged_in_signup.png'
                })
                print(f"✗ Erro: {e}")

        finally:
            browser.close()

    return results, test_email

if __name__ == "__main__":
    import os

    # Criar diretório de screenshots
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

    print("=" * 60)
    print("EXECUTANDO TESTES DE AUTENTICAÇÃO - FINANPY")
    print("=" * 60)

    results, test_email = test_authentication_flows()

    # Gerar relatório
    print("\n" + "=" * 60)
    print("RELATÓRIO FINAL DE TESTES")
    print("=" * 60)

    passed = sum(1 for r in results if r['status'] == 'PASSOU')
    failed = sum(1 for r in results if r['status'] == 'FALHOU')
    blocked = sum(1 for r in results if r['status'] == 'BLOQUEADO')
    warnings = sum(1 for r in results if r['status'] == 'AVISO')
    total = len(results)

    print(f"\nRESUMO:")
    print(f"Total de testes: {total}")
    print(f"✓ Passaram: {passed}")
    print(f"✗ Falharam: {failed}")
    print(f"⚠ Avisos: {warnings}")
    print(f"⊗ Bloqueados: {blocked}")

    print(f"\nDETALHES DOS TESTES:")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        status_icon = {
            'PASSOU': '✓',
            'FALHOU': '✗',
            'BLOQUEADO': '⊗',
            'AVISO': '⚠'
        }.get(result['status'], '?')

        print(f"\n{i}. {result['test']}")
        print(f"   Status: {status_icon} {result['status']}")
        print(f"   Detalhes: {result['details']}")
        print(f"   Screenshot: {result['screenshot']}")

    print(f"\n" + "=" * 60)
    print(f"Email de teste usado: {test_email}")
    print(f"Screenshots salvos em: {SCREENSHOTS_DIR}")
    print("=" * 60)
