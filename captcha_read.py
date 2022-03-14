from captcha_solver import CaptchaSolver

solver = CaptchaSolver('https://captchasolver.com/api/status/X19R0NJK8SROTJR0WOOIVEX6S')
raw_data = open('captcha_images/1.png', 'rb').read()
print(solver.solve_captcha(raw_data))
