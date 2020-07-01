/* MdpmflcTutorial - simple driver that demos how to write drivers 
 * compatible with mdpmflc (https://github.com/jftsang/mdpmflc). 
 */
#include <iostream>
#include <fstream>
#include <map>

#include "Mercury3D.h"
#include "Particles/SphericalParticle.h"
#include "Species/LinearViscoelasticFrictionSpecies.h"

using namespace std;


class MdpmflcTutorial : public Mercury3D
{
    public:

        MdpmflcTutorial(string parsfile)
        {
            /* Read the parameters file and save its contents as a map. 
             * TODO: Support default parameters.
             */
            ifstream file(parsfile);
            string name; double var;
            while (file >> name >> var) {
                pars[name] = var;
            }

            /* Importantly, the .data. and .fstat. files need to be 
             * saved across multiple files. 
             */
            dataFile.setFileType(FileType::MULTIPLE_FILES);
            fStatFile.setFileType(FileType::MULTIPLE_FILES);
            
            /* Other ctor stuff (you could put these in setupInitialConditions). 
             * Use parameters from the parameters file. 
             */
            /* Set the name of the simulation */
            setName(parsfile.erase(parsfile.find_last_of('.')));

            if (pars.find("random_seed") != pars.end())
                random.setRandomSeed(int(pars.at("random_seed")));
            else
                random.randomise();

            setTimeStep(0.001);
            setTimeMax(10);
            setSaveCount(1000);
            setSystemDimensions(3);

            setXMin(0);
            setXMax(pars.at("xmax"));
            setYMin(0);
            setYMax(pars.at("ymax"));
            setZMin(0);
            setZMax(pars.at("zmax")); 

            species_ = new LinearViscoelasticFrictionSpecies();
            species_->setDensity(1);
            species_->setCollisionTimeAndRestitutionCoefficient(
                        0.01, pars.at("restitution_coeff"),
                        (4.0/3.0) * constants::pi * pow(pars.at("particle_radius"), 3)
                      );
            species_ = speciesHandler.copyAndAddObject(species_);

            particle_ = new SphericalParticle();
            particle_->setSpecies(species_);
            particle_->setRadius(pars.at("particle_radius"));
            particle_ = particleHandler.copyAndAddObject(particle_);

            setGravity(Vec3D(0, 0, -1));
        }

    private:
        map<string,double> pars;
        LinearViscoelasticFrictionSpecies *species_;
        SphericalParticle *particle_;

};

int main(int argc, char *argv[])  // we *don't* want const int, const char
{
    if (argc > 1)
    {
        auto problem = new MdpmflcTutorial((string)argv[1]);  // pass the parsfile filename
        argv[1] = argv[0];  // feed the rest of the command line arguments
        problem->solve(argc-1, argv+1);
        delete problem;
        return 0;
    }
    else
    {
        fprintf(stderr, "Usage: %s parsfile [options]\n", argv[0]);
        exit(-1);
    }
}
