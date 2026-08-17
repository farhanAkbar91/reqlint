describe('ReqLint SRS Editor & Audit Flow (E2E QA)', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should load the SRS Requirement Editor UI', () => {
    cy.contains('ReqLint').should('be.visible');
    cy.get('#srs-requirement-input').should('be.visible');
  });

  it('should analyze Indonesian requirement and show audit scorecard', () => {
    cy.get('#srs-requirement-input')
      .clear()
      .type('Sistem sebaiknya dapat memproses data transaksi pengguna dengan cepat.');
    
    cy.contains('Run ReqLint Audit').click();

    // Verify Audit Scorecard & Smells
    cy.contains('Quality Scorecard').should('be.visible');
    cy.contains('LANG: ID').should('be.visible');
    cy.contains('WEAK_DIRECTIVE_ID').should('be.visible');
  });

  it('should analyze English requirement and detect ambiguity smells', () => {
    cy.get('#srs-requirement-input')
      .clear()
      .type('The system should process user payment data quickly.');
    
    cy.contains('Run ReqLint Audit').click();

    // Verify English detection & smells
    cy.contains('Quality Scorecard').should('be.visible');
    cy.contains('LANG: EN').should('be.visible');
    cy.contains('WEAK_DIRECTIVE_EN').should('be.visible');
  });
});
