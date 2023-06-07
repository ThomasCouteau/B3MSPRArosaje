describe("Arosaje", () => {
  beforeEach(() => {
    // Init la taille de l'écran
    cy.viewport(1440, 900);
    cy.visit("http://localhost:8080/");
  });

  it("Authentification", () => {
    // Clique sur le bouton "OK" de la popup
    cy.contains("OK").click();

    // Saisir le nom d'utilisateur et le mot de passe
    cy.get('input[name="Login"]').type("Nicolas");
    cy.get('input[name="password"]').type("mspr");

    // Cliquer sur le bouton de soumission
    cy.get('button[type="button"]').click();

    // Vérifier la redirection vers la page d'accueil
    cy.url().should("eq", "http://localhost:8080/home");
  });

  it("Ajouter un post", () => {
    // Clique sur le bouton "OK" de la popup
    cy.contains("OK").click();

    // Saisir le nom d'utilisateur et le mot de passe
    cy.get('input[name="Login"]').type("Nicolas");
    cy.get('input[name="password"]').type("mspr");

    // Cliquer sur le bouton de soumission
    cy.get('button[type="button"]').click();

    // Vérifier la redirection vers la page d'accueil
    cy.url().should("eq", "http://localhost:8080/home");

    // Clique sur le bouton "Créer"
    cy.get('a[name="Créer"]').click();

    // Saisir le nom d'une plante
    cy.get('input[name="name"]').type("Une plante de test");

    // Cliquer sur le bouton de soumission
    cy.get('button[name="createPost"]').click();

    // Vérifier la redirection vers la page d'accueil
    cy.url().should("eq", "http://localhost:8080/home");
  });

  it("Supprimer un post", () => {
    // Clique sur le bouton "OK" de la popup
    cy.contains("OK").click();

    // Saisir le nom d'utilisateur et le mot de passe
    cy.get('input[name="Login"]').type("Nicolas");
    cy.get('input[name="password"]').type("mspr");

    // Cliquer sur le bouton de soumission
    cy.get('button[type="button"]').click();

    // Vérifier la redirection vers la page d'accueil
    cy.url().should("eq", "http://localhost:8080/home");

    // Aller sur le profil
    cy.visit("http://localhost:8080/profile");

    //Supprime le post
    cy.get('button[name="threePoints"]').first().click();
    cy.get('div[name="deletePost"]').click();

    // Vérifier la redirection vers la page du profil
    cy.url().should("eq", "http://localhost:8080/profile");
  });
});
