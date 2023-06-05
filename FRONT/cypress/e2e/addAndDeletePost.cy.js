describe('Ajoute et supprime un post', () => {
  beforeEach(() => {
    //Init la taille de l'écran
    cy.viewport(1440, 900);
    // Visiter le site
    cy.visit("http://localhost:8080/home");
  });

  it("Ajoute un post et le supprime", () => {
    // Clique sur le bouton "Créer"
    cy.contains("Créer").click();

    // Saisir le nom d'une plante
    cy.get('input[name="name"]').type("Une plante de test");

    // Cliquer sur le bouton de soumission
    cy.get('button[name="createPost"]').click();

    // Vérifier la redirection vers la page d'accueil
    cy.url().should("eq", "http://localhost:8080/search");
  });
})
