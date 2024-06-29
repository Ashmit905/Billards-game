#include <stdlib.h>
#include "phylib.h"
#include <math.h>
#include <string.h>
#include <stdio.h>

// PART 1 OF THE ASSIGNMENT

phylib_object *phylib_new_still_ball(unsigned char number,
                                     phylib_coord *pos)
{
    // Defining local variables
    phylib_object *createSpace = NULL;

    // Allocating memory
    createSpace = malloc(sizeof(phylib_object));

    // NULL Check here to ensure that
    if (createSpace == NULL)
    {
        return NULL;
    }

    createSpace->type = 0;
    createSpace->obj.still_ball.pos = *pos;
    createSpace->obj.still_ball.number = number;

    return createSpace;
}

phylib_object *phylib_new_rolling_ball(unsigned char number,
                                       phylib_coord *pos,
                                       phylib_coord *vel,
                                       phylib_coord *acc)
{
    // Defining local Variables
    phylib_object *allocateSpace = NULL;

    // Allocating memory
    allocateSpace = malloc(sizeof(phylib_object));

    // Do a Null check here
    if (allocateSpace == NULL)
    {
        return NULL;
    }

    allocateSpace->type = 1;
    allocateSpace->obj.rolling_ball.pos = *pos;
    allocateSpace->obj.rolling_ball.number = number;
    allocateSpace->obj.rolling_ball.vel = *vel;
    allocateSpace->obj.rolling_ball.acc = *acc;

    return allocateSpace;
}

phylib_object *phylib_new_hole(phylib_coord *pos)
{
    // defining local variables

    phylib_object *spaceCreate = NULL;

    // Allocating space for memory
    spaceCreate = malloc(sizeof(phylib_object));

    // do a NULL check here
    if (spaceCreate == NULL)
    {
        return NULL;
    }
    spaceCreate->type = PHYLIB_HOLE;
    spaceCreate->obj.hole.pos = *pos;

    return spaceCreate;
}

phylib_object *phylib_new_hcushion(double y)
{

    // Defining local Variables

    phylib_object *spaceAllocate = NULL;

    spaceAllocate = malloc(sizeof(phylib_object));

    // do a NULL check here

    if (spaceAllocate == NULL)
    {
        return NULL;
    }

    // spaceAllocate->obj.hcushion = 3;
    spaceAllocate->type = PHYLIB_HCUSHION;
    spaceAllocate->obj.hcushion.y = y;

    // Return pointer
    return spaceAllocate;
}

phylib_object *phylib_new_vcushion(double x)
{

    // Defining Local Variables

    phylib_object *newSpace = NULL;

    // Allocate space for memory
    newSpace = malloc(sizeof(phylib_object));

    // Do a NULL check here
    if (newSpace == NULL)
    {
        return NULL;
    }
    newSpace->type = PHYLIB_VCUSHION;
    newSpace->obj.vcushion.x = x;
    // Return pointer
    return newSpace;
}

phylib_table *phylib_new_table(void)
{

    // Defining local Variables

    phylib_table *createTable = NULL;

    // Allocate space for memory

    createTable = (phylib_table *)calloc(1, sizeof(phylib_table));

    if (createTable == NULL)
    {
        return NULL; // Memory Allocation failed
    }

    // This is setting the member variable to 0.0 as specified
    createTable->time = 0.0;

    // creating the objects

    // 1. Horizontal cushion at y =0.0
    createTable->object[0] = phylib_new_hcushion(0.0);

    // 2. Horizontal cushion at at y=PHYLIB_Table_Lengh

    createTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    // 3. a vertical cushion at x=0.0

    createTable->object[2] = phylib_new_vcushion(0.0);

    // 4. a vertical cushion at x= PHYLIB_TABLE_WIDTH

    createTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // 5. 6 holes: positioned in the four corners where the cushions meet and two more
    // midway between the top holes and bottom holes

    createTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});                                    // Top Left
    createTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH / 2});                // left
    createTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});                    // Top Right
    createTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_LENGTH / 2, 0.0});                // Bottom Left
    createTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2}); // Midway bottom
    createTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});     // Bottom Right
    // Set the remaining Objects to NULL
    // Set remaining pointers to NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; ++i)
    {
        createTable->object[i] = NULL;
    }

    return createTable;
}

// PART 2 Function Definitions

void phylib_copy_object(phylib_object **dest, phylib_object **src)
{
    // Allocate memory for phylib_object
    *dest = calloc(1, sizeof(phylib_object));

    if (*dest != NULL && *src != NULL)
    {
        memcpy(*dest, *src, sizeof(phylib_object));
    }
    else
    {
        // Handle the case where either src or dest is NULL
        free(*dest); // Free the allocated memory
        *dest = NULL;
    }
}

phylib_table *phylib_copy_table(phylib_table *table)
{
    if (table == NULL)
    {
        return NULL;
    }
    // Defining local Variables

    phylib_table *tableNew = calloc(1, sizeof(phylib_table));
    // do a NULL check
    if (tableNew == NULL)
    {
        return NULL; // Memory Allocation has failed!
    }

    tableNew->time = table->time;
    for (int x = 0; x < PHYLIB_MAX_OBJECTS; x++)
    {
        if (table->object[x] != NULL)
        {
            phylib_copy_object(&tableNew->object[x], &table->object[x]);
        }
    }

    // return the pointer
    return tableNew;
}

void phylib_add_object(phylib_table *table, phylib_object *object)
{

    // loop over the objects and do a null check
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }
    }
}

void phylib_free_table(phylib_table *table)
{

    // iterate over the objects until you free the object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
        }
    }
    // Free the table itself
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    // Declaring local Variables
    phylib_coord determineResult;

    // calculate the result between the x values
    determineResult.x = c1.x - c2.x;

    // Calculate the result between the y values
    determineResult.y = c1.y - c2.y;

    return determineResult;
}

double phylib_length(phylib_coord c)
{

    // equation for length
    return sqrt(c.x * c.x + c.y * c.y);
}

double phylib_dot_product(phylib_coord a, phylib_coord b)
{

    // equation for the dot product
    return a.x * b.x + a.y * b.y;
}

// Finish the last function for Part 2

double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{

    if (obj1 == NULL || obj2 == NULL)
    {
        return -1.0;
    }

    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0;
    }

    phylib_coord ballPosition = obj1->obj.rolling_ball.pos;

    if (obj2->type == PHYLIB_STILL_BALL)
    {
        // calc diff between centre of both balls
        phylib_coord newVariable = phylib_sub(ballPosition, obj2->obj.still_ball.pos);
        return phylib_length(newVariable) - PHYLIB_BALL_DIAMETER;
    }

    if (obj2->type == PHYLIB_ROLLING_BALL)
    {

        // Calc diff between centre of both balls
        phylib_coord variableNew = phylib_sub(ballPosition, obj2->obj.rolling_ball.pos);
        return phylib_length(variableNew) - PHYLIB_BALL_DIAMETER;
    }

    if (obj2->type == PHYLIB_HOLE)
    {
        phylib_coord radiusBall = phylib_sub(ballPosition, obj2->obj.hole.pos);
        return phylib_length(radiusBall) - PHYLIB_HOLE_RADIUS;
    }

    if (obj2->type == PHYLIB_VCUSHION)
    {
        // returns absolute values with decimal points
        return fabs(ballPosition.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
    }

    if (obj2->type == PHYLIB_HCUSHION)
    {
        // return absolute balues with decimal points
        return fabs(ballPosition.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
    }

    return -1.0;
}

// PART 3 FUNCTIONS

void phylib_roll(phylib_object *new, phylib_object *old, double time)

{

    double multiplyTime = time * time;

    if (new->type != PHYLIB_ROLLING_BALL && old->type != PHYLIB_ROLLING_BALL)
    {
        return;
    }

    // Here we are applying all the equations specified in the pdf doc
    else
    {
        new->obj.rolling_ball.pos.x = (old->obj.rolling_ball.pos.x) + (old->obj.rolling_ball.vel.x * time) + (0.5 * old->obj.rolling_ball.acc.x * multiplyTime);
        new->obj.rolling_ball.pos.y = (old->obj.rolling_ball.pos.y) + (old->obj.rolling_ball.vel.y * time) + (0.5 * old->obj.rolling_ball.acc.y * multiplyTime);

        new->obj.rolling_ball.vel.x = (old->obj.rolling_ball.vel.x) + (old->obj.rolling_ball.acc.x * time);
        new->obj.rolling_ball.vel.y = (old->obj.rolling_ball.vel.y) + (old->obj.rolling_ball.acc.y * time);

        if (new->obj.rolling_ball.vel.x >= 0 && old->obj.rolling_ball.vel.x <= 0)
        {
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }

        if (new->obj.rolling_ball.vel.x <= 0 && old->obj.rolling_ball.vel.x >= 0)
        {

            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }

        if (new->obj.rolling_ball.vel.y >= 0 && old->obj.rolling_ball.vel.y <= 0)
        {
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }

        if (new->obj.rolling_ball.vel.y <= 0 && old->obj.rolling_ball.vel.y >= 0)
        {

            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }
    }
}

unsigned char phylib_stopped(phylib_object *object)
{
    if (object->type == PHYLIB_ROLLING_BALL)
    {
        double velocityMagnitude = phylib_length(object->obj.rolling_ball.vel);

        if (velocityMagnitude < PHYLIB_VEL_EPSILON)
        {
            // If the velocity magnitude is below the threshold, consider it stopped
            phylib_coord positionBall = object->obj.rolling_ball.pos;
            phylib_object *newObject = phylib_new_still_ball(object->obj.rolling_ball.number, &positionBall);

            // Update the contents of the original object
            object->type = newObject->type;
            object->obj.still_ball = newObject->obj.still_ball;

            // Free the memory allocated for the new object
            free(newObject);

            return 1; // Object has stopped
        }
    }

    return 0; // Object is still rolling
}

void phylib_bounce(phylib_object **a, phylib_object **b)
{

    // Case 1: b is a h cushion
    if ((*b)->type == PHYLIB_HCUSHION)
    {
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
    }

    // Case 2: b is a v cushion

    else if ((*b)->type == PHYLIB_VCUSHION)
    {
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
    }

    // Case 3: b is a hole
    else if ((*b)->type == PHYLIB_HOLE)
    {
        free(*a);
        *a = NULL;
    }

    // Case 4: b is a still ball
    else if ((*b)->type == PHYLIB_STILL_BALL)
    {

        phylib_object *oldObject;
        oldObject = *b;

        phylib_coord coord = (*b)->obj.rolling_ball.pos;
        phylib_coord vel;
        vel.x = 0;
        vel.y = 0;
        phylib_coord acc;
        acc.x = 0;
        acc.y = 0;
        (*b) = phylib_new_rolling_ball((*b)->obj.still_ball.number, &coord, &vel, &acc);

        free(oldObject);
    }

    // Case 5: b is a rolling ball

    if ((*b)->type == PHYLIB_ROLLING_BALL)
    {
        phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
        phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
        phylib_coord n = {r_ab.x / phylib_length(r_ab), r_ab.y / phylib_length(r_ab)};
        double v_rel_n = phylib_dot_product(v_rel, n);

        // Update the velocities of a and b

        (*a)->obj.rolling_ball.vel.x -= (v_rel_n * n.x);
        (*a)->obj.rolling_ball.vel.y -= (v_rel_n * n.y);
        (*b)->obj.rolling_ball.vel.x += (v_rel_n * n.x);
        (*b)->obj.rolling_ball.vel.y += (v_rel_n * n.y);

        // Compute speeds

        double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
        double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

        // Check if Speed a is greater then Phylib_vel_epsilon

        if (speed_a > PHYLIB_VEL_EPSILON)
        {
            (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / (speed_a)*PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / (speed_a)*PHYLIB_DRAG;
        }

        // check if speed b is greater then phylib_vel_epsilon

        if (speed_b > PHYLIB_VEL_EPSILON)
        {
            (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / (speed_b)*PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / (speed_b)*PHYLIB_DRAG;
        }
    }
}

unsigned char phylib_rolling(phylib_table *t)
{

    // Declaring local variables
    int countRolling = 0;

    // iterate through the objects whule type is rolling ball and increment
    for (int k = 0; k < PHYLIB_MAX_OBJECTS; k++)
    {
        if (t->object[k] != NULL && t->object[k]->type == PHYLIB_ROLLING_BALL)
        {
            countRolling++;
        }
    }

    return countRolling;
}

phylib_table *phylib_segment(phylib_table *table)
{

    // call the rolling function along with a NULL check
    int rollBall = phylib_rolling(table);

    if (rollBall == 0)
    {
        return NULL;
    }

    // Create a copy of the table
    phylib_table *tableNew = phylib_copy_table(table);

    // create a time variable
    double time = PHYLIB_SIM_RATE;

    // Loop over the time loop
    while (time < PHYLIB_MAX_TIME)
    {

        // loop over the objects
        for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
        {
            // set the object to type of rolling ball
            if (tableNew->object[j] != NULL && tableNew->object[j]->type == PHYLIB_ROLLING_BALL)
            {
                // call the phylib roll function
                phylib_roll(tableNew->object[j], table->object[j], time);

                // call the phylib stopped function
                if (phylib_stopped(tableNew->object[j]) == 1)
                {
                    // increment the time
                    tableNew->time += time;
                    return tableNew;
                }
            }
        }

        // loop over the objects
        for (int x = 0; x < PHYLIB_MAX_OBJECTS; x++)
        {
            // set to type rolling ball
            if (tableNew->object[x] != NULL && tableNew->object[x]->type == PHYLIB_ROLLING_BALL)
            {
                for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
                {
                    if (x != i && tableNew->object[i] != NULL && phylib_distance(tableNew->object[x], tableNew->object[i]) < 0.0)
                    {
                        // call the bounce function and increment time
                        phylib_bounce(&tableNew->object[x], &tableNew->object[i]);

                        if (tableNew->object[i])
                        {
                            phylib_stopped(tableNew->object[i]);
                        }
                        tableNew->time += time;
                        return tableNew;
                    }
                }
            }
        }

        // increment time
        time += PHYLIB_SIM_RATE;
    }
    // return the new table
    return tableNew;
}

// A2 starts here

// Function provided by the profS

char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        sprintf(string, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        sprintf(string,
                "STILL_BALL (%d,%6.1lf,%6.1lf)",
                object->obj.still_ball.number,
                object->obj.still_ball.pos.x,
                object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        sprintf(string,
                "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                object->obj.rolling_ball.number,
                object->obj.rolling_ball.pos.x,
                object->obj.rolling_ball.pos.y,
                object->obj.rolling_ball.vel.x,
                object->obj.rolling_ball.vel.y,
                object->obj.rolling_ball.acc.x,
                object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        sprintf(string,
                "HOLE (%6.1lf,%6.1lf)",
                object->obj.hole.pos.x,
                object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        sprintf(string,
                "HCUSHION (%6.1lf)",
                object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        sprintf(string,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x);
        break;
    }
    return string;
}
