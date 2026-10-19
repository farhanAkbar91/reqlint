describe('ReqLint Agile User Story Editor & INVEST Audit Flow (E2E QA)', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should load the Agile User Story Editor UI', () => {
    cy.contains('ReqLint').should('be.visible');
    cy.get('#user-story-input').should('be.visible');
  });

  it('should analyze Indonesian User Story and show INVEST audit scorecard', () => {
    cy.get('#user-story-input')
      .clear()
      .type('Sebagai pembeli, saya sebaiknya dapat membayar dengan cepat, sehingga transaksi segera selesai.');
    
    cy.contains('Audit User Story').click();

    // Verify INVEST Quality Scorecard & Smells
    cy.contains('INVEST Quality Scorecard').should('be.visible');
    cy.contains('BAHASA: ID').should('be.visible');
    cy.contains('WEAK_DIRECTIVE_ID').should('be.visible');
    cy.contains('SUBJECTIVE_ADJECTIVE_ID').should('be.visible');
  });

  it('should analyze English User Story and detect INVEST ambiguity smells', () => {
    cy.get('#user-story-input')
      .clear()
      .type('As a buyer, I should be able to checkout easily, so that I save time.');
    
    cy.contains('Audit User Story').click();

    // Verify English detection & smells
    cy.contains('INVEST Quality Scorecard').should('be.visible');
    cy.contains('BAHASA: EN').should('be.visible');
    cy.contains('WEAK_DIRECTIVE_EN').should('be.visible');
    cy.contains('SUBJECTIVE_ADJECTIVE_EN').should('be.visible');
  });
});

