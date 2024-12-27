import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FenetreRadiologueComponent } from './fenetre-radiologue.component';

describe('FenetreRadiologueComponent', () => {
  let component: FenetreRadiologueComponent;
  let fixture: ComponentFixture<FenetreRadiologueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FenetreRadiologueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FenetreRadiologueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
