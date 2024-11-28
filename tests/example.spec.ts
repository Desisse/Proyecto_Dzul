import { test, expect } from '@playwright/test';
import { register } from 'module';

// test('has title', async ({ page }) => {
//   await page.goto('https://playwright.dev/');

//   // Expect a title "to contain" a substring.
//   await expect(page).toHaveTitle(/Playwright/);
// });

// test('get started link', async ({ page }) => {
//   await page.goto('https://playwright.dev/');
//   await page.pause();

//   // Click the get started link.
//   await page.getByRole('link', { name: 'Get started' }).click();
//   await page.pause();

//   // Expects page to have a heading with the name of Installation.
//   await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
//   await page.pause();
// });

//PRUEBA 1
//Ingresamos al navegador
// test('navigate to registration page and register', async ({ page }) => {
//   // Navegar a la página principal
//   await page.goto('https://www.cyberpuerta.mx/?gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V-_2gCMouPwuLdIbXYBJ-BqeLIdH7tlZUZMUs0_uXjMy4gjcRRhOfUaApkSEALw_wcB');
//   await page.pause();
//   //Pagina de cuenta
//   const loginTitle = page.locator('div.oxwidget_headerlogin_title1');
//   await expect(loginTitle).toBeVisible();
//   await loginTitle.click();
//   await page.waitForTimeout(3000);
//   await page.pause();
//   //Boton para registrarse
//   const registerButton = page.locator('a.normalButton.largeButton.oxwidget_headerlogin_register_button');
//   await expect(registerButton).toBeVisible({ timeout: 10000 }); 
//   console.log('Botón de registro localizado.');
//   //Click boton registro
//   await registerButton.click();
//   console.log('Clic en el botón de registro.');
//   await page.pause();
//   //Llenar formulario
//   const nameInput = page.locator('input#name'); // Campo de nombre
//   const emailInput = page.locator('input#email'); // Campo de email
//   const passwordInput = page.locator('input#password'); // Campo de contraseña
//   const confirmPasswordInput = page.locator('input#confirm-password'); // Confirmar contraseña
//   const createAccountButton = page.locator('button.create-account-btn'); // Botón "Crear cuenta"

//   // Llenar los campos del formulario
//   await expect(nameInput).toBeVisible({ timeout: 10000 });
//   await nameInput.fill('Angel Nava'); 
//   console.log('Campo de nombre llenado.');

//   await expect(emailInput).toBeVisible({ timeout: 10000 });
//   await emailInput.fill('angel.ene02@hotmail.com'); 
//   console.log('Campo de email llenado.');

//   await expect(passwordInput).toBeVisible({ timeout: 10000 });
//   await passwordInput.fill('Angel-Zorro02'); 
//   console.log('Campo de contraseña llenado.');
//   await page.pause();

//   await expect(confirmPasswordInput).toBeVisible({ timeout: 10000 });
//   await confirmPasswordInput.fill('Angel-Zorro02'); 
//   console.log('Campo de confirmación de contraseña llenado.');
//   await page.pause();

//   //Boton crear cuenta
//   await expect(createAccountButton).toBeVisible({ timeout: 10000 });
//   await createAccountButton.click();
//   console.log('Crear cuenta');
//   await page.pause();

//Prueba 2
// test('navigate to registration page and register', async ({ page }) => {
//     // Navegar a la página principal
//     await page.goto('https://www.cyberpuerta.mx/?gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V-_2gCMouPwuLdIbXYBJ-BqeLIdH7tlZUZMUs0_uXjMy4gjcRRhOfUaApkSEALw_wcB');
//     await page.pause();
//     //Pagina de cuenta
//     const loginTitle = page.locator('div.oxwidget_headerlogin_title1');
//     await expect(loginTitle).toBeVisible();
//     await loginTitle.click();
//     await page.waitForTimeout(3000);
//     await page.pause();
//     // Localizar el campo de entrada por su ID
//     const emailInput = page.locator('input#loginEmail');

//     // Verificar que el campo de entrada sea visible
//     await expect(emailInput).toBeVisible({ timeout: 10000 });

//     // Llenar el campo con un valor
//     await emailInput.fill('angel.ene02@hotmail.com');
//     console.log('Campo de email llenado.');
//     await page.pause();
//     // Localizar el campo de contraseña con el ID corregido y llenarlo
//     const passwordInput = page.locator('input#loginPasword'); // ID corregido
//     await expect(passwordInput).toBeVisible({ timeout: 10000 });
//     await passwordInput.fill('Angel-Zorro02');
//     console.log('Campo de contraseña llenado.');
//     await page.pause();
//     // Selector del botón usando su texto único
//     const submitButton = page.locator('button:has-text("Iniciar sesión")');
//     await expect(submitButton).toBeVisible({ timeout: 10000 });
//     await submitButton.click();
//     console.log('Botón "Iniciar sesión" clicado.');
//     await page.pause();


//     // Buscar el campo de búsqueda por su placeholder único
// const searchInput = page.getByPlaceholder('¿Qué producto buscas el día de hoy?');

// // Verificar que el campo de búsqueda es visible
// await expect(searchInput).toBeVisible({ timeout: 10000 });
// console.log('Campo de búsqueda visible.');

// // Llenar el campo de búsqueda con la palabra "gabinete"
// await searchInput.fill('gabinete');
// console.log('Campo de búsqueda llenado con "gabinete".');

// // Localizar y hacer clic en el botón de búsqueda (ícono de lupa)
// const searchButton = page.locator('button:has-text("Buscar")'); // Ajusta el selector según el sitio.
// await expect(searchButton).toBeVisible({ timeout: 10000 });
// await searchButton.click();
// console.log('Clic en el botón de búsqueda.');

//   // Localizar el componente con id="productList-1"
//   const productList = page.locator('#productList-1');

//   // Verificar que el componente sea visible
//   await expect(productList).toBeVisible({ timeout: 10000 });
//   console.log('Componente con id="productList-1" es visible.');

//   // Realizar clic en el componente
//   await productList.click();
//   console.log('Clic en el componente con id="productList-1".');
//   await page.pause();
  
//   // Localizar el botón "Agregar al carrito" usando el atributo data-pre-process-add-to-cart
//   const addToCartButton = page.locator('button[data-pre-process-add-to-cart="5206f39a002830e5dcd4a3edf5c3b9cf"]'); //Ojo aquí, porque el componente del carrito puede cambiar, entonces si pasa eso modificarlo

//   // Verificar que el botón sea visible
//   await expect(addToCartButton).toBeVisible({ timeout: 10000 });
//   console.log('Botón "Agregar al carrito" localizado.');

//   // Realizar clic en el botón "Agregar al carrito"
//   await addToCartButton.click();
//   console.log('Clic en el botón "Agregar al carrito".');
//   await page.pause();

//Prueba 3 iniciar sesion, seleccionar un producto, agregarlo a la lista de deseos y ver la lista de deseos
test('navigate to registration page and register', async ({ page }) => {
      // Navegar a la página principal
      await page.goto('https://www.cyberpuerta.mx/?gad_source=1&gclid=Cj0KCQiAgJa6BhCOARIsAMiL7V-_2gCMouPwuLdIbXYBJ-BqeLIdH7tlZUZMUs0_uXjMy4gjcRRhOfUaApkSEALw_wcB');
      await page.pause();
      const loginTitle = page.locator('div.oxwidget_headerlogin_title1');
    await expect(loginTitle).toBeVisible();
    await loginTitle.click();
    await page.waitForTimeout(3000);
    await page.pause();
    // Localizar el campo de entrada por su ID
    const emailInput = page.locator('input#loginEmail');

    // Verificar que el campo de entrada sea visible
    await expect(emailInput).toBeVisible({ timeout: 10000 });

    // Llenar el campo con un valor
    await emailInput.fill('angel.ene02@hotmail.com');
    console.log('Campo de email llenado.');
    await page.pause();
    // Localizar el campo de contraseña con el ID corregido y llenarlo
    const passwordInput = page.locator('input#loginPasword'); // ID corregido
    await expect(passwordInput).toBeVisible({ timeout: 10000 });
    await passwordInput.fill('Angel-Zorro02');
    console.log('Campo de contraseña llenado.');
    await page.pause();
    //Selector del botón usando su texto único
    const submitButton = page.locator('button:has-text("Iniciar sesión")');
    await expect(submitButton).toBeVisible({ timeout: 10000 });
    await submitButton.click();
    console.log('Botón "Iniciar sesión" clicado.');
    
    // Buscar el campo de búsqueda por su placeholder único
    const searchInput = page.getByPlaceholder('¿Qué producto buscas el día de hoy?');

    // Verificar que el campo de búsqueda es visible
    await expect(searchInput).toBeVisible({ timeout: 10000 });
    console.log('Campo de búsqueda visible.');

    // Llenar el campo de búsqueda con la palabra "gabinete"
    await searchInput.fill('monitores');
    console.log('Campo de búsqueda llenado con "monitores".');

    // Localizar y hacer clic en el botón de búsqueda (ícono de lupa)
    const searchButton = page.locator('button:has-text("Buscar")'); // Ajusta el selector según el sitio.
    await expect(searchButton).toBeVisible({ timeout: 10000 });
    await searchButton.click();
    console.log('Clic en el botón de búsqueda.');
    await page.pause();
    // Interactuar con el producto usando su id "productList-1"
    const productSelector = page.locator('#productList-1');  // Usamos el ID del producto
    await expect(productSelector).toBeVisible({ timeout: 10000 });
    await productSelector.click();  // Hacer clic en el producto
    console.log('Producto seleccionado.');
    await page.pause();

    const addToFavoritesLink = page.locator('a:has-text("Guardar en favoritos")');
    await expect(addToFavoritesLink).toBeVisible({ timeout: 10000 });
    await addToFavoritesLink.click();
    console.log('Producto agregado a favoritos.');
    await page.pause();

    //Ojo aquí, porque solo funciona si no hay ningún articulo guardado en favoritos, de preferencia que esté vacío
    const closeButton = page.locator('[title="Close"]');
    await expect(closeButton).toBeVisible({ timeout: 10000 });  // Verificar si es visible
    await closeButton.click();  // Hacer clic para cerrar el recuadro
    console.log('Recuadro cerrado.');
    await page.pause();

    const favoritesTitle = page.locator('div.oxwidget_headernotice_title1:has-text("Favoritos")');
    await expect(favoritesTitle).toBeVisible({ timeout: 10000 });
    await favoritesTitle.click();
    console.log('Favoritos abiertos.');
    await page.pause();
    // Seleccionar el primer enlace con la clase 'normalButton' y el texto 'Ver lista'
    const viewListButton = page.locator('.normalButton:has-text("Ver lista")').nth(0);

    // Verificar que el botón sea visible
    await expect(viewListButton).toBeVisible({ timeout: 10000 });

    // Hacer clic en el botón
    await viewListButton.click();
    console.log('Lista de favoritos abierta.');
    await page.pause();
});
